# index_options_bot/risk/risk_manager.py

from datetime import datetime, timedelta


class RiskManager:
    """
    Enforces all capital & discipline rules.
    AUTHORITATIVE component.
    """

    def __init__(self, max_trades_per_day, max_loss_per_day, cooldown_minutes):
        self.max_trades_per_day = max_trades_per_day
        self.max_loss_per_day = max_loss_per_day
        self.cooldown_minutes = cooldown_minutes

        self.trades_taken = 0
        self.realized_pnl = 0.0
        self.last_sl_time = None

    def can_take_trade(self):
        """
        Called BEFORE placing a trade
        """

        # Max trades check
        if self.trades_taken >= self.max_trades_per_day:
            print("[RISK] Max trades per day reached")
            return False

        # Max loss check
        if abs(self.realized_pnl) >= self.max_loss_per_day:
            print("[RISK] Max loss per day reached")
            return False

        # Cool-off check
        if self.last_sl_time:
            next_allowed_time = self.last_sl_time + timedelta(
                minutes=self.cooldown_minutes
            )
            if datetime.now() < next_allowed_time:
                remaining = (next_allowed_time - datetime.now()).seconds
                print(f"[RISK] Cool-off active ({remaining}s remaining)")
                return False

        return True

    def register_trade(self):
        """
        Called AFTER order entry
        """
        self.trades_taken += 1
        print(f"[RISK] Trades taken today: {self.trades_taken}")

    def register_exit(self, pnl, exit_reason):
        """
        Called AFTER trade exit
        """
        self.realized_pnl += pnl
        print(f"[RISK] Realized PnL: {self.realized_pnl}")

        if exit_reason == "TRAILING_SL":
            self.last_sl_time = datetime.now()
            print(
                f"[RISK] SL hit → Cool-off started for "
                f"{self.cooldown_minutes} minutes"
            )
