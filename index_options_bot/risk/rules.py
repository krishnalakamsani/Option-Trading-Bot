# index_option_bot/risk/rules.py

MAX_LOSS_PER_TRADE = 1000        # ₹
MAX_LOSS_PER_DAY = 3000          # ₹
MAX_TRADES_PER_DAY = 5
MAX_CONSECUTIVE_LOSSES = 2

RISK_PER_TRADE_PCT = 1           # % of capital
TRAILING_SL_PCT = 0.3            # 30% trail
COOLDOWN_AFTER_LOSS_MIN = 15

MARKET_START = "09:20"
MARKET_END = "15:15"

