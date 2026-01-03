# Index Options Trading Bot

Automated trading bot for Indian index options (NIFTY) using Dhan broker API.

## Features

- ✅ **SuperTrend Strategy**: Trade based on SuperTrend indicator (customizable period & multiplier)
- ✅ **Paper Trading**: Simulate trades without real money
- ✅ **Live Trading**: Execute real trades via Dhan API (with toggle)
- ✅ **Risk Management**: Stop loss, trailing stop, max trades/day, max loss/day
- ✅ **Offline-Safe**: Instrument data cached locally
- ✅ **Auto Expiry Detection**: Automatically selects nearest weekly expiry
- ✅ **ATM Strike Selection**: Calculates ATM strike based on index price
- ✅ **Kill-Switch**: Instantly disable trading
- ✅ **Comprehensive Logging**: All actions logged to files
- ✅ **Data Storage**: Trades saved in both CSV and JSON formats

## Project Structure

```
index_options_bot/
├── config/
│   └── settings.py          # Configuration management
├── data/
│   ├── instruments/         # NFO instrument master data
│   ├── trades/              # Trade logs (CSV + JSON)
│   └── pnl/                 # PnL reports
├── strategy/
│   └── supertrend.py        # SuperTrend strategy implementation
├── execution/
│   ├── paper.py             # Paper trading engine
│   └── live.py              # Live trading engine
├── risk/
│   └── risk_manager.py      # Risk management system
├── utils/
│   ├── dhan_client.py       # Dhan API wrapper
│   ├── instruments.py       # Instrument management
│   └── market_time.py       # Market timing utilities
├── logs/                    # Bot execution logs
├── main.py                  # Main bot orchestrator
├── requirements.txt         # Python dependencies
└── .env                     # Configuration file
```

## Installation

1. **Install Python dependencies**:
```bash
cd /app/index_options_bot
pip install -r requirements.txt
```

2. **Configure the bot**:
Edit `.env` file with your settings:
```bash
# Dhan API Credentials (REQUIRED)
DHAN_CLIENT_ID=your_client_id
DHAN_ACCESS_TOKEN=your_access_token

# Trading Mode: 'paper' or 'live'
TRADING_MODE=paper

# Risk Management
STOP_LOSS_PERCENT=30
TRAILING_STOP_PERCENT=10
MAX_TRADES_PER_DAY=20
MAX_LOSS_PER_DAY=20000

# SuperTrend Strategy
SUPERTREND_PERIOD=7
SUPERTREND_MULTIPLIER=4
CANDLE_TIMEFRAME=1
```

## Usage

### Run the Bot

```bash
python main.py
```

### Switch Between Paper and Live Trading

Edit `.env`:
```bash
# For paper trading (recommended first)
TRADING_MODE=paper

# For live trading (REAL MONEY)
TRADING_MODE=live
```

### Monitor Logs

```bash
# View today's log
tail -f logs/bot_$(date +%Y%m%d).log

# View all logs
ls -lh logs/
```

### View Trades

```bash
# View today's trades (JSON)
cat data/trades/trades_$(date +%Y-%m-%d).json

# View today's trades (CSV)
cat data/trades/trades_$(date +%Y-%m-%d).csv
```

## Configuration Options

### Risk Parameters

- `STOP_LOSS_PERCENT`: Maximum loss % per trade (default: 30%)
- `TRAILING_STOP_PERCENT`: Trailing stop loss % (default: 10%)
- `MAX_TRADES_PER_DAY`: Maximum trades allowed per day (default: 20)
- `MAX_LOSS_PER_DAY`: Maximum loss in INR per day (default: 20000)

### Strategy Parameters

- `SUPERTREND_PERIOD`: SuperTrend period (default: 7)
- `SUPERTREND_MULTIPLIER`: SuperTrend multiplier (default: 4)
- `CANDLE_TIMEFRAME`: Candle timeframe in minutes (default: 1)

### Trading Parameters

- `INDEX_NAME`: Index to trade (default: NIFTY)
- `LOT_SIZE`: Lots per trade (default: 10)
- `POLLING_INTERVAL`: Price polling interval in seconds (default: 1)

## How It Works

1. **Initialization**:
   - Authenticates with Dhan API
   - Downloads/loads NFO instruments
   - Initializes strategy and risk manager

2. **Trading Cycle** (every polling interval):
   - Fetches index LTP
   - Calculates ATM strike
   - Fetches option price
   - Calculates SuperTrend indicator
   - Generates buy/sell signals
   - Executes trades (paper or live)
   - Updates positions and checks stops

3. **Risk Management**:
   - Monitors stop loss and trailing stop
   - Enforces max trades per day
   - Enforces max loss per day
   - Provides kill-switch functionality

## SuperTrend Strategy

The bot uses the SuperTrend indicator to identify trends:

- **BUY Signal**: When price crosses above SuperTrend (uptrend starts)
- **SELL Signal**: When price crosses below SuperTrend (downtrend starts)

The indicator is calculated using:
- ATR (Average True Range) for volatility
- Period and Multiplier for sensitivity

## Safety Features

1. **Paper Trading First**: Always test with paper trading before going live
2. **Kill-Switch**: Instantly stop all trading
3. **Daily Limits**: Maximum trades and loss limits
4. **Stop Loss**: Per-trade stop loss
5. **Trailing Stop**: Lock in profits as price moves favorably
6. **Market Hours Check**: Prevents trading when market is closed
7. **Comprehensive Logging**: Full audit trail of all actions

## Getting Dhan API Credentials

1. Open a Dhan trading account at https://dhan.co
2. Go to Settings > API Management
3. Generate API credentials (Client ID and Access Token)
4. Add them to the `.env` file

## Important Notes

⚠️ **WARNING**: 
- This bot trades REAL MONEY when in live mode
- Always test thoroughly in paper trading mode first
- Understand the risks of algorithmic trading
- Monitor the bot regularly
- Start with small position sizes

📊 **Performance**:
- Past performance doesn't guarantee future results
- Markets can be volatile and unpredictable
- Use appropriate position sizing and risk management

🔧 **Maintenance**:
- Update instrument data regularly
- Monitor logs for errors
- Review and adjust strategy parameters based on market conditions

## Troubleshooting

### Authentication Failed
- Verify Dhan credentials in `.env`
- Check if API access is enabled in your Dhan account
- Ensure access token hasn't expired

### No Valid Expiry Found
- Update instrument data: delete `data/instruments/nfo_instruments.csv` and restart
- Check if it's a trading holiday

### Bot Not Generating Signals
- Ensure sufficient price data (need at least 7 candles for default period)
- Check if market is open
- Review strategy parameters in `.env`

## Future Enhancements

- [ ] WebSocket streaming for real-time data
- [ ] ML-based strategy models
- [ ] Multiple indices support (BANKNIFTY, FINNIFTY)
- [ ] Dashboard/UI for monitoring
- [ ] Database storage (MongoDB/PostgreSQL)
- [ ] Backtesting framework
- [ ] Alert notifications (Email/SMS/Telegram)
- [ ] Advanced order types (limit, stop-limit)
- [ ] Multi-leg strategies (spreads, straddles)

## License

MIT License - Use at your own risk

## Disclaimer

This bot is for educational and research purposes only. Trading in financial markets involves substantial risk of loss. The creators are not responsible for any financial losses incurred while using this bot. Always consult with a qualified financial advisor before trading.