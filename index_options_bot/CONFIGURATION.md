# Configuration Guide

## Complete Configuration Reference

### Dhan API Credentials

```bash
DHAN_CLIENT_ID=your_client_id_here
DHAN_ACCESS_TOKEN=your_access_token_here
```

**How to get Dhan credentials:**
1. Open Dhan trading account at https://dhan.co
2. Login to your account
3. Go to Settings → API Management
4. Click "Generate API Credentials"
5. Copy Client ID and Access Token
6. Paste in `.env` file

**Security Notes:**
- Never share your credentials
- Never commit `.env` file to git
- Tokens may expire - regenerate if needed
- Keep credentials secure

---

### Trading Mode

```bash
TRADING_MODE=paper  # or 'live'
```

**Options:**
- `paper`: Simulated trading (recommended first)
  - No real money involved
  - Tests strategy safely
  - Generates realistic logs
  - Same logic as live mode

- `live`: Real trading (use with caution)
  - Executes real orders
  - Uses real money
  - Requires valid Dhan credentials
  - Monitor closely

**Best Practice:**
1. Start with paper mode for 1-2 weeks
2. Review trades and performance
3. Tune parameters based on results
4. Switch to live with small lot sizes
5. Scale up gradually

---

### Index Configuration

```bash
INDEX_NAME=NIFTY
LOT_SIZE=10
STRIKE_INTERVAL=50
```

**INDEX_NAME**: Which index to trade
- Current: `NIFTY`
- Future: `BANKNIFTY`, `FINNIFTY` (not yet implemented)

**LOT_SIZE**: Number of lots per trade
- Range: 1-50 (higher = more risk)
- Recommended start: 1-2 lots
- Current: 10 lots
- Each NIFTY lot = 25 shares (verify current lot size)

**STRIKE_INTERVAL**: Strike price interval
- NIFTY: 50 points
- BANKNIFTY: 100 points (typically)
- Used for ATM calculation

---

### Risk Management

```bash
STOP_LOSS_PERCENT=30
TRAILING_STOP_PERCENT=10
MAX_TRADES_PER_DAY=20
MAX_LOSS_PER_DAY=20000
```

#### Stop Loss Percent
- Absolute stop loss per trade
- Current: 30% (aggressive)
- Conservative: 15-20%
- Moderate: 20-30%
- Aggressive: 30-40%

**Example:** 
- Entry: ₹100
- Stop Loss (30%): ₹70
- If price drops to ₹70, position closes automatically

#### Trailing Stop Percent
- Locks in profits as price moves favorably
- Current: 10%
- Conservative: 5-8%
- Moderate: 8-12%
- Aggressive: 12-15%

**Example:**
- Entry: ₹100
- Price rises to ₹150
- Trailing stop: ₹135 (10% below peak)
- If price drops to ₹135, position closes with profit

#### Max Trades Per Day
- Maximum number of trades allowed daily
- Current: 20
- Conservative: 3-5
- Moderate: 5-10
- Aggressive: 10-20+

**Purpose:** Prevents overtrading

#### Max Loss Per Day
- Maximum loss allowed per day (in ₹)
- Current: ₹20,000
- Set based on your capital
- Recommended: 2-5% of total capital

**Example:**
- Capital: ₹500,000
- Max Loss: ₹20,000 (4%)
- Once hit, bot stops trading for the day

---

### SuperTrend Strategy

```bash
SUPERTREND_PERIOD=7
SUPERTREND_MULTIPLIER=4
CANDLE_TIMEFRAME=1
```

#### Period
- Number of candles for ATR calculation
- Current: 7
- Lower (5-7): More signals, more noise
- Medium (7-14): Balanced
- Higher (14-21): Fewer signals, more reliable

**Effect:**
- Period 5: Very responsive, many trades
- Period 10: Moderate trades
- Period 20: Few but strong signals

#### Multiplier
- Distance of SuperTrend from price
- Current: 4
- Lower (2-3): Closer to price, more signals
- Medium (3-4): Balanced
- Higher (4-5): Further from price, fewer signals

**Effect:**
- Multiplier 2: Frequent signals
- Multiplier 3: Moderate signals
- Multiplier 5: Rare but strong signals

#### Candle Timeframe
- Timeframe for each candle (in minutes)
- Current: 1 minute
- Options: 1, 3, 5, 15, 30, 60
- Lower: More granular, more trades
- Higher: Less granular, fewer trades

**Example:**
- 1-min: Scalping, many trades
- 5-min: Intraday, moderate trades
- 15-min: Positional, few trades

---

### System Configuration

```bash
POLLING_INTERVAL=1
```

#### Polling Interval
- How often to check prices (in seconds)
- Current: 1 second
- Minimum: 1 second
- Maximum: 60 seconds
- Recommended: 1-5 seconds

**Impact:**
- 1 sec: Fast response, more API calls
- 5 sec: Balanced
- 60 sec: Slow response, fewer API calls

---

## Strategy Parameter Combinations

### Conservative Setup
```bash
STOP_LOSS_PERCENT=20
TRAILING_STOP_PERCENT=8
MAX_TRADES_PER_DAY=5
MAX_LOSS_PER_DAY=10000
LOT_SIZE=1
SUPERTREND_PERIOD=14
SUPERTREND_MULTIPLIER=3
CANDLE_TIMEFRAME=5
```
- Fewer trades
- Tighter stops
- Less risk

### Moderate Setup (Current)
```bash
STOP_LOSS_PERCENT=30
TRAILING_STOP_PERCENT=10
MAX_TRADES_PER_DAY=20
MAX_LOSS_PER_DAY=20000
LOT_SIZE=10
SUPERTREND_PERIOD=7
SUPERTREND_MULTIPLIER=4
CANDLE_TIMEFRAME=1
```
- Balanced approach
- Moderate risk/reward

### Aggressive Setup
```bash
STOP_LOSS_PERCENT=40
TRAILING_STOP_PERCENT=15
MAX_TRADES_PER_DAY=30
MAX_LOSS_PER_DAY=30000
LOT_SIZE=20
SUPERTREND_PERIOD=5
SUPERTREND_MULTIPLIER=2
CANDLE_TIMEFRAME=1
```
- Many trades
- Higher risk/reward

---

## Parameter Tuning Guide

### Step 1: Start Conservative
- Use conservative parameters
- Run in paper mode for 1 week
- Monitor performance

### Step 2: Analyze Results
```bash
# View trades
cat data/trades/trades_*.json

# Calculate win rate
python -c "
import json, glob
trades = []
for f in glob.glob('data/trades/trades_*.json'):
    trades.extend(json.load(open(f)))

wins = [t for t in trades if t.get('pnl', 0) > 0]
losses = [t for t in trades if t.get('pnl', 0) < 0]

print(f'Total Trades: {len(trades)}')
print(f'Wins: {len(wins)} ({len(wins)/len(trades)*100:.1f}%)')
print(f'Losses: {len(losses)} ({len(losses)/len(trades)*100:.1f}%)')
print(f'Avg Win: ₹{sum(t[\"pnl\"] for t in wins)/len(wins):.2f}')
print(f'Avg Loss: ₹{sum(t[\"pnl\"] for t in losses)/len(losses):.2f}')
"
```

### Step 3: Adjust Parameters
- If too many trades → Increase period/multiplier
- If too few trades → Decrease period/multiplier
- If many losses → Tighten stop loss
- If missing profits → Adjust trailing stop

### Step 4: Test Again
- Apply changes to `.env`
- Run for another week
- Compare results

### Step 5: Iterate
- Repeat until satisfied
- Move to live trading with small lots
- Continue monitoring

---

## Configuration Validation

Before running:
```bash
# Test configuration
python test_bot.py

# Check file
cat .env

# Validate credentials (will fail if invalid)
python -c "
from config.settings import config
from utils.dhan_client import DhanClient

config.validate()
print('✓ Config valid')

client = DhanClient()
if client.authenticate():
    print('✓ Credentials valid')
else:
    print('✗ Credentials invalid')
"
```

---

## Environment Variables Priority

1. `.env` file (highest priority)
2. System environment variables
3. Default values in code

To override:
```bash
# One-time override
TRADING_MODE=live python main.py

# Or export
export TRADING_MODE=live
python main.py
```

---

## Configuration Backup

```bash
# Backup current config
cp .env .env.backup.$(date +%Y%m%d)

# Restore from backup
cp .env.backup.20260103 .env
```

---

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] Credentials are not hardcoded
- [ ] `.env` has proper permissions (chmod 600)
- [ ] Backup `.env` is secure
- [ ] Never share `.env` file
- [ ] Regenerate tokens if compromised

---

## Quick Reference

| Parameter | Conservative | Moderate | Aggressive |
|-----------|--------------|----------|------------|
| Stop Loss % | 15-20 | 20-30 | 30-40 |
| Trailing Stop % | 5-8 | 8-12 | 12-15 |
| Max Trades/Day | 3-5 | 5-10 | 10-20+ |
| Lot Size | 1-2 | 2-5 | 5-20 |
| ST Period | 14-21 | 7-14 | 5-7 |
| ST Multiplier | 3-4 | 3-4 | 2-3 |
| Candle Time | 5-15 min | 3-5 min | 1-3 min |
