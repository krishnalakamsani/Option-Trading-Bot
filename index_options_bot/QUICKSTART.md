# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
cd /app/index_options_bot
pip install -r requirements.txt
```

### Step 2: Configure

The bot is already configured with your settings:

```bash
# View configuration
cat .env
```

Your current settings:
- **Trading Mode**: Paper (Simulated)
- **Index**: NIFTY
- **Lot Size**: 10
- **Stop Loss**: 30%
- **Trailing Stop**: 10%
- **Max Trades/Day**: 20
- **Max Loss/Day**: ₹20,000
- **SuperTrend**: Period=7, Multiplier=4, 1-min candles

### Step 3: Run

```bash
# Test components first (recommended)
python test_bot.py

# Run the bot
python main.py
```

## 📊 Understanding the Output

When you run the bot, you'll see:

```
============================================================
INDEX OPTIONS TRADING BOT - INITIALIZATION
============================================================

✓ Configuration validated
✓ Authentication successful
✓ Instruments loaded
✓ Strategy initialized
✓ Trading mode: PAPER

============================================================
✓ BOT INITIALIZATION COMPLETE
============================================================

--- Iteration 1 [09:15:30] ---
Index LTP: 23500
Option LTP: ₹152.34
Daily Summary: Trades=0/20, PnL=₹0.00

--- Iteration 2 [09:15:31] ---
...
```

### When Signals Occur

**Buy Signal**:
```
🟢 BUY SIGNAL: Price crossed above SuperTrend at 155.50
💰 PAPER BUY: NIFTY 2025-01-09 23500 CE @ ₹155.50 x 10
✓ BUY order placed
```

**Sell Signal**:
```
🔴 SELL SIGNAL: Price crossed below SuperTrend at 145.20
💸 PAPER SELL: NIFTY 2025-01-09 23500 CE @ ₹145.20 x 10
✓ Position closed: SIGNAL, PnL: ₹-103.00
```

**Stop Loss Hit**:
```
⚠️ Stop Loss hit: ₹140.50 <= ₹142.00
✓ Position closed: STOP_LOSS, PnL: ₹-150.00
```

## 🎯 Trading Logic

The bot follows this logic every second:

1. **Fetch Data**
   - Get NIFTY index price
   - Calculate ATM strike
   - Get option price

2. **Calculate SuperTrend**
   - Build price candles (1-min)
   - Calculate indicator
   - Determine trend direction

3. **Generate Signals**
   - **BUY**: When price crosses ABOVE SuperTrend (uptrend starts)
   - **SELL**: When price crosses BELOW SuperTrend (downtrend starts)

4. **Risk Checks**
   - Check max trades limit
   - Check max loss limit
   - Check stop loss
   - Check trailing stop

5. **Execute**
   - Place order (paper or live)
   - Track position
   - Log everything

## 📁 Where to Find Data

### Logs
```bash
# Today's log
cat logs/bot_$(date +%Y%m%d).log

# Watch live
tail -f logs/bot_$(date +%Y%m%d).log
```

### Trades
```bash
# JSON format (detailed)
cat data/trades/trades_$(date +%Y-%m-%d).json

# CSV format (spreadsheet-friendly)
cat data/trades/trades_$(date +%Y-%m-%d).csv
```

### Instruments
```bash
# NFO instrument master
cat data/instruments/nfo_instruments.csv
```

## 🎚️ Customizing Settings

Edit `.env` file:

```bash
# Make it more aggressive
STOP_LOSS_PERCENT=40
MAX_TRADES_PER_DAY=30

# Make it more conservative
STOP_LOSS_PERCENT=20
MAX_TRADES_PER_DAY=5

# Change strategy parameters
SUPERTREND_PERIOD=10
SUPERTREND_MULTIPLIER=3

# Switch to different timeframe
CANDLE_TIMEFRAME=3  # 3-minute candles
```

After editing, restart the bot.

## ⚠️ Before Going Live

1. **Test Thoroughly**
   ```bash
   # Run in paper mode for at least 1-2 weeks
   TRADING_MODE=paper python main.py
   ```

2. **Review Trades**
   ```bash
   # Check performance
   cat data/trades/trades_*.json
   ```

3. **Start Small**
   ```bash
   # Reduce lot size for live testing
   LOT_SIZE=1
   ```

4. **Enable Live Trading**
   ```bash
   # Edit .env
   TRADING_MODE=live
   
   # Run
   python main.py
   ```

5. **Monitor Closely**
   - Keep terminal open
   - Watch logs in real-time
   - Be ready to stop if needed (Ctrl+C)

## 🛑 Emergency Stop

Press `Ctrl+C` to stop the bot gracefully.

The bot will:
- Stop accepting new trades
- Close open positions (in production)
- Save final summary
- Exit cleanly

## 🔧 Troubleshooting

### "Authentication failed"
→ Check Dhan credentials in `.env`
→ Verify API access is enabled in Dhan account

### "No valid expiry found"
→ Delete `data/instruments/nfo_instruments.csv`
→ Restart bot (it will re-download)

### "Market is CLOSED"
→ Normal. Bot will continue in demo mode
→ Wait for market hours (9:15 AM - 3:30 PM IST, Mon-Fri)

### Bot not generating signals
→ Need at least 7 candles (7 minutes with 1-min timeframe)
→ Wait a few minutes after starting

## 📈 Performance Monitoring

### Daily Summary
```bash
# View final summary
grep "FINAL SUMMARY" logs/bot_*.log
```

### Calculate PnL
```bash
# From trades file
python -c "
import json
with open('data/trades/trades_$(date +%Y-%m-%d).json') as f:
    trades = json.load(f)
    pnl = sum(t.get('pnl', 0) for t in trades)
    print(f'Total PnL: ₹{pnl:.2f}')
"
```

## 🎓 Next Steps

1. **Backtest** (Future): Run on historical data
2. **Optimize**: Tune SuperTrend parameters
3. **Add Features**: Multiple strategies, indices
4. **Build UI**: Dashboard for monitoring
5. **Enhance**: Add alerts, notifications

## 📞 Support

- Review logs for errors
- Check README.md for detailed documentation
- Ensure Dhan API is accessible
- Test with `test_bot.py` first

---

**Remember**: This bot trades REAL MONEY in live mode. Always test thoroughly in paper mode first!
