# index_options_bot/positions/position_manager.py

import time

from index_options_bot.risk.trailing_sl import TrailingSL
from index_options_bot.utils.dhan_client import get_ltp
from index_options_bot.utils.market_time import is_market_open


class PositionManager:
    """
    Owns the FULL lifecycle of a position:
    ENTRY already done
    → Monitor price
    → Update trailing SL
    → Exit when SL hits
    """

    def __init__(self, executor, trail_points, poll_interval=1):
        self.executor = executor
        self.trailing_sl = TrailingSL(trail_points)
        self.poll_interval = poll_interval

    def manage(self, position):
        print(f"[POSITION] Started managing {position.symbol}")

        while position.is_open and is_market_open():
            ltp = get_ltp(position.symbol)

            # Update trailing SL
            new_sl = self.trailing_sl.update_sl(
                ltp=ltp,
                current_sl=position.sl
            )

            if new_sl != position.sl:
                print(f"[SL] {position.symbol} SL moved {position.sl} → {new_sl}")
                position.sl = new_sl

            # Exit condition
            if ltp <= position.sl:
                print(f"[EXIT] SL hit for {position.symbol} at {ltp}")

                self.executor.exit(
                    symbol=position.symbol,
                    qty=position.qty
                )

                position.close(price=ltp, reason="TRAILING_SL")
                break

            time.sleep(self.poll_interval)

        return position
