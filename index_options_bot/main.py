# index_options_bot/main.py

from index_options_bot.strategy.supertrend import check_signal
from index_options_bot.positions.position import Position
from index_options_bot.positions.position_manager import PositionManager
from index_options_bot.execution.paper_executor import PaperExecutor
from index_options_bot.risk.risk_manager import RiskManager
from index_options_bot.pnl.trade_logger import TradeLogger
from index_options_bot.pnl.daily_summary import DailyPnLSummary
from index_options_bot.utils.market_time import is_market_open


# ===== CONFIG =====
INITIAL_SL_POINTS = 10
TRAIL_SL_POINTS = 5
QTY = 50

MAX_TRADES_PER_DAY = 3
MAX_LOSS_PER_DAY = 2000
COOLDOWN_MINUTES = 10
# ==================


def main():
    print("[SYSTEM] Bot started")

    if not is_market_open():
        print("[SYSTEM] Market is closed")
        return

    executor = PaperExecutor()

    risk_manager = RiskManager(
        max_trades_per_day=MAX_TRADES_PER_DAY,
        max_loss_per_day=MAX_LOSS_PER_DAY,
        cooldown_minutes=COOLDOWN_MINUTES
    )

    trade_logger = TradeLogger()
    daily_summary = DailyPnLSummary()

    # 1️⃣ Signal
    signal = check_signal()
    if not signal:
        print("[SYSTEM] No trade signal")
        return

    # 2️⃣ Risk check (includes cool-off)
    if not risk_manager.can_take_trade():
        print("[SYSTEM] Trade blocked by risk rules")
        return

    symbol = signal["symbol"]
    print(f"[SIGNAL] BUY signal for {symbol}")

    # 3️⃣ Entry
    order = executor.buy(symbol=symbol, qty=QTY)
    entry_price = order["price"]

    risk_manager.register_trade()

    position = Position(
        symbol=symbol,
        qty=QTY,
        entry_price=entry_price,
        sl=entry_price - INITIAL_SL_POINTS
    )

    # 4️⃣ Manage position
    position_manager = PositionManager(
        executor=executor,
        trail_points=TRAIL_SL_POINTS,
        poll_interval=1
    )

    final_position = position_manager.manage(position)

    # 5️⃣ PnL
    pnl = (final_position.exit_price - entry_price) * QTY
    print(f"[PNL] Trade PnL: {pnl}")

    # 6️⃣ Update systems
    risk_manager.register_exit(pnl, final_position.exit_reason)

    trade_logger.log_trade(
        symbol=symbol,
        qty=QTY,
        entry_price=entry_price,
        exit_price=final_position.exit_price,
        pnl=pnl,
        exit_reason=final_position.exit_reason
    )

    daily_summary.update(pnl)

    print(
        f"[RESULT] Exit Reason: {final_position.exit_reason}, "
        f"Exit Price: {final_position.exit_price}"
    )


if __name__ == "__main__":
    main()
