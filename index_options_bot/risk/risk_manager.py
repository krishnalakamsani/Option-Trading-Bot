# index_option_bot/risk/risk_manager.py

from datetime import datetime
from .rules import *

class RiskManager:
    def __init__(self, capital):
        self.capital = capital
        self.daily_pnl = 0
        self.trades_today = 0
        self.consecutive_losses = 0
        self.last_loss_time = None

    def can_trade(self):
        if self.daily_pnl <= -MAX_LOSS_PER_DAY:
            return False, "Daily loss limit hit"

        if self.trades_today >= MAX_TRADES_PER_DAY:
            return False, "Max trades reached"

        if self.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            return False, "Consecutive loss limit"

        if self._cooldown_active():
            return False, "Cooldown active"

        return True, "Allowed"

    def register_trade(self):
        self.trades_today += 1

    def update_pnl(self, pnl):
        self.daily_pnl += pnl
        if pnl < 0:
            self.consecutive_losses += 1
            self.last_loss_time = datetime.now()
        else:
            self.consecutive_losses = 0

    def _cooldown_active(self):
        if not self.last_loss_time:
            return False
        minutes = (datetime.now() - self.last_loss_time).seconds / 60
        return minutes < COOLDOWN_AFTER_LOSS_MIN
