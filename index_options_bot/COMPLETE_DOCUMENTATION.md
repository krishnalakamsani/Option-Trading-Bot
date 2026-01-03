# Index Options Trading Bot - Complete Documentation

**Version:** 1.0.0  
**Last Updated:** January 3, 2026  
**Author:** Automated Trading System  
**License:** MIT

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Architecture](#architecture)
7. [Module Reference](#module-reference)
8. [Strategy Guide](#strategy-guide)
9. [Risk Management](#risk-management)
10. [Usage Guide](#usage-guide)
11. [Deployment](#deployment)
12. [Monitoring & Logs](#monitoring--logs)
13. [Troubleshooting](#troubleshooting)
14. [Performance Optimization](#performance-optimization)
15. [Security Best Practices](#security-best-practices)
16. [API Reference](#api-reference)
17. [FAQ](#faq)
18. [Changelog](#changelog)

---

## Overview

The Index Options Trading Bot is a production-ready, automated trading system designed for Indian index options markets. It uses the SuperTrend technical indicator to generate trading signals and executes trades through the Dhan broker API.

### Key Highlights

- **Market**: NSE Index Options (NIFTY, future: BANKNIFTY, FINNIFTY)
- **Strategy**: SuperTrend indicator-based
- **Broker**: Dhan (via official Python SDK)
- **Trading Modes**: Paper trading (simulation) and Live trading
- **Risk Management**: Stop loss, trailing stop, daily limits
- **Architecture**: Modular, extensible, production-ready

### Design Philosophy

1. **Safety First**: Paper trading by default, comprehensive risk controls
2. **Modular**: Easy to extend with new strategies or features
3. **Transparent**: Comprehensive logging of all decisions
4. **Reliable**: Graceful error handling, restart-safe
5. **Configurable**: All parameters externalized to .env

---

## Features

### Core Trading Features

✅ **SuperTrend Strategy**
- Custom implementation (no external dependency)
- Configurable period and multiplier
- Automatic signal generation on trend changes

✅ **Dual Trading Modes**
- Paper trading for safe testing
- Live trading for real execution
- Easy toggle between modes

✅ **Smart Option Selection**
- Automatic expiry detection (nearest weekly)
- ATM strike calculation
- Fallback to next expiry if needed

✅ **Real-time Monitoring**
- Price polling at configurable intervals
- Position tracking
- P&L calculation

### Risk Management

✅ **Multi-level Protection**
- Absolute stop loss (percentage-based)
- Trailing stop loss (locks in profits)
- Maximum trades per day limit
- Maximum loss per day limit
- Kill-switch for emergency halt

✅ **Position Management**
- Single position at a time (for safety)
- Automatic position closure on stops
- Entry/exit price tracking

### Data Management

✅ **Comprehensive Logging**
- File-based logs with rotation
- Timestamped entries
- Multiple log levels (INFO, WARNING, ERROR)

✅ **Trade Storage**
- Dual format: CSV and JSON
- Daily trade files
- Complete trade history

✅ **Instrument Data**
- Local caching of NFO instruments
- Offline-safe operation
- Auto-refresh capability

### System Features

✅ **Market Intelligence**
- Market hours validation
- IST timezone handling
- Trading holiday awareness (via market check)

✅ **Reliability**
- Graceful shutdown (SIGINT/SIGTERM)
- Error recovery
- Restart-safe design

✅ **Monitoring**
- Real-time status updates
- Daily summary reports
- Performance metrics

---

## System Requirements

### Minimum Requirements

- **OS**: Linux (Ubuntu 20.04+), macOS, Windows 10+
- **Python**: 3.11+
- **RAM**: 512 MB
- **Disk**: 1 GB free space
- **Network**: Stable internet connection

### Recommended Requirements

- **OS**: Linux (Ubuntu 22.04)
- **Python**: 3.11
- **RAM**: 1 GB
- **Disk**: 5 GB free space
- **Network**: Low-latency connection (<50ms to NSE)

### Dependencies

```
dhanhq==2.0.2          # Dhan broker API
pandas==2.3.3          # Data manipulation
numpy==2.4.0           # Numerical computing
python-dotenv==1.2.1   # Environment variables
pytz==2025.2           # Timezone handling
```

---

## Installation

### Step 1: System Setup

```bash
# Update system (Linux)
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 (if not installed)
sudo apt install python3.11 python3.11-venv python3-pip -y
```

### Step 2: Clone/Download Project

**Option A: From GitHub**
```bash
git clone https://github.com/yourusername/index-options-bot.git
cd index-options-bot/index_options_bot
```

**Option B: From ZIP**
```bash
unzip index-options-bot.zip
cd index_options_bot
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Copy example .env
cp .env.example .env  # If provided

# Or create new .env
nano .env
```

Add your configuration:
```bash
DHAN_CLIENT_ID=your_client_id
DHAN_ACCESS_TOKEN=your_access_token
TRADING_MODE=paper
# ... (see Configuration section)
```

### Step 6: Verify Installation

```bash
python test_bot.py
```

Expected output:
```
✓ Configuration: PASSED
✓ Market Time: PASSED
✓ SuperTrend Strategy: PASSED

✓ All tests passed! Bot is ready to run.
```

---

## Configuration

### Environment Variables (.env)

#### Dhan API Credentials

```bash
DHAN_CLIENT_ID=your_client_id_here
DHAN_ACCESS_TOKEN=your_access_token_here
```

**How to obtain:**
1. Login to Dhan: https://dhan.co
2. Settings → API Management
3. Generate API credentials
4. Copy Client ID and Access Token

#### Trading Mode

```bash
TRADING_MODE=paper
```

**Options:**
- `paper`: Simulated trading (recommended for testing)
- `live`: Real trading with real money

#### Index Configuration

```bash
INDEX_NAME=NIFTY
LOT_SIZE=10
STRIKE_INTERVAL=50
```

**Parameters:**
- `INDEX_NAME`: Which index to trade (NIFTY, BANKNIFTY, etc.)
- `LOT_SIZE`: Number of lots per trade (1 NIFTY lot = 25 shares)
- `STRIKE_INTERVAL`: Strike price interval (NIFTY: 50, BANKNIFTY: 100)

#### Risk Management

```bash
STOP_LOSS_PERCENT=30
TRAILING_STOP_PERCENT=10
MAX_TRADES_PER_DAY=20
MAX_LOSS_PER_DAY=20000
```

**Parameters:**
- `STOP_LOSS_PERCENT`: Maximum loss per trade (%)
- `TRAILING_STOP_PERCENT`: Trailing stop distance (%)
- `MAX_TRADES_PER_DAY`: Daily trade limit
- `MAX_LOSS_PER_DAY`: Daily loss limit (₹)

#### SuperTrend Strategy

```bash
SUPERTREND_PERIOD=7
SUPERTREND_MULTIPLIER=4
CANDLE_TIMEFRAME=1
```

**Parameters:**
- `SUPERTREND_PERIOD`: Number of candles for ATR calculation
- `SUPERTREND_MULTIPLIER`: Distance multiplier from price
- `CANDLE_TIMEFRAME`: Candle duration (minutes)

#### System Settings

```bash
POLLING_INTERVAL=1
```

**Parameters:**
- `POLLING_INTERVAL`: Price check frequency (seconds)

### Configuration Presets

#### Conservative Trading
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

#### Moderate Trading (Default)
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

#### Aggressive Trading
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

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│                    Main Bot                         │
│                  (main.py)                          │
└──────────┬──────────────────────────────┬───────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│   Configuration      │      │   Dhan API Client    │
│   (config/)          │      │   (utils/)           │
└──────────────────────┘      └──────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Strategy Engine     │      │  Instrument Manager  │
│  (strategy/)         │      │  (utils/)            │
└──────────────────────┘      └──────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Risk Manager        │      │  Market Time Utils   │
│  (risk/)             │      │  (utils/)            │
└──────────────────────┘      └──────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│         Execution Engine                             │
│  ┌──────────────┐         ┌──────────────┐          │
│  │ Paper Trading│         │ Live Trading │          │
│  │ (execution/) │         │ (execution/) │          │
│  └──────────────┘         └──────────────┘          │
└──────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│                  Data Layer                          │
│  ├─ Logs/                                            │
│  ├─ Trades/ (CSV + JSON)                             │
│  └─ Instruments/                                     │
└──────────────────────────────────────────────────────┘
```

### Directory Structure

```
index_options_bot/
│
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py            # Centralized config
│
├── strategy/                   # Trading strategies
│   ├── __init__.py
│   └── supertrend.py          # SuperTrend implementation
│
├── execution/                  # Order execution
│   ├── __init__.py
│   ├── paper.py               # Paper trading
│   └── live.py                # Live trading
│
├── risk/                       # Risk management
│   ├── __init__.py
│   └── risk_manager.py        # Risk controls
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── dhan_client.py         # Dhan API wrapper
│   ├── instruments.py         # Instrument management
│   └── market_time.py         # Market timing
│
├── data/                       # Data storage
│   ├── instruments/           # Cached instruments
│   ├── trades/                # Trade history
│   └── pnl/                   # P&L reports
│
├── logs/                       # Log files
│
├── main.py                     # Main orchestrator
├── test_bot.py                 # Component tests
├── run_bot.sh                  # Convenience script
├── requirements.txt            # Dependencies
├── .env                        # Configuration
└── .gitignore                  # Git ignore rules
```

### Component Descriptions

#### Main Bot (main.py)
- **Purpose**: Orchestrates all components
- **Responsibilities**: 
  - Initialize all modules
  - Run main trading loop
  - Handle signals and shutdown
  - Coordinate between components

#### Configuration (config/settings.py)
- **Purpose**: Centralized configuration management
- **Features**:
  - Load from .env file
  - Validate configuration
  - Provide config object to all modules

#### Dhan Client (utils/dhan_client.py)
- **Purpose**: Wrapper for Dhan API
- **Features**:
  - Authentication
  - Get fund limits
  - Fetch LTP (Last Traded Price)
  - Place orders
  - Get order status

#### Instrument Manager (utils/instruments.py)
- **Purpose**: Manage NFO instruments
- **Features**:
  - Download instrument master
  - Cache locally (offline-safe)
  - Filter options by underlying
  - Find nearest expiry
  - Calculate ATM strike
  - Get security IDs

#### Market Time (utils/market_time.py)
- **Purpose**: Market timing utilities
- **Features**:
  - Check if market is open
  - Get current IST time
  - Calculate time to market open

#### SuperTrend Strategy (strategy/supertrend.py)
- **Purpose**: Implement SuperTrend indicator
- **Features**:
  - Calculate True Range (TR)
  - Calculate ATR (Average True Range)
  - Calculate SuperTrend bands
  - Generate buy/sell signals
  - Track trend direction

#### Risk Manager (risk/risk_manager.py)
- **Purpose**: Enforce risk controls
- **Features**:
  - Check trade limits (daily max)
  - Check loss limits (daily max)
  - Track positions
  - Calculate stop loss
  - Calculate trailing stop
  - Kill-switch functionality

#### Paper Trading (execution/paper.py)
- **Purpose**: Simulate order execution
- **Features**:
  - Virtual order placement
  - Virtual position tracking
  - Trade logging
  - P&L calculation

#### Live Trading (execution/live.py)
- **Purpose**: Real order execution
- **Features**:
  - Place market orders via Dhan
  - Get order status
  - Enable/disable live trading
  - Safety checks

---

## Module Reference

### config.settings

```python
from config.settings import config

# Access configuration
client_id = config.DHAN_CLIENT_ID
trading_mode = config.TRADING_MODE
lot_size = config.LOT_SIZE

# Validate configuration
config.validate()  # Raises exception if invalid
```

**Available Properties:**
- `DHAN_CLIENT_ID`: str
- `DHAN_ACCESS_TOKEN`: str
- `TRADING_MODE`: str ('paper' or 'live')
- `INDEX_NAME`: str
- `LOT_SIZE`: int
- `STRIKE_INTERVAL`: int
- `STOP_LOSS_PERCENT`: float
- `TRAILING_STOP_PERCENT`: float
- `MAX_TRADES_PER_DAY`: int
- `MAX_LOSS_PER_DAY`: float
- `SUPERTREND_PERIOD`: int
- `SUPERTREND_MULTIPLIER`: float
- `CANDLE_TIMEFRAME`: int
- `POLLING_INTERVAL`: int
- Directory paths (DATA_DIR, LOGS_DIR, etc.)

### utils.dhan_client.DhanClient

```python
from utils.dhan_client import DhanClient

# Initialize
client = DhanClient()

# Authenticate
success = client.authenticate()

# Get fund limits
funds = client.get_fund_limits()

# Get LTP
ltp = client.get_ltp(security_id, exchange_segment)

# Place order
response = client.place_order(
    security_id='123456',
    exchange_segment='NSE_FNO',
    transaction_type='BUY',
    quantity=25,
    order_type='MARKET',
    product_type='INTRADAY'
)
```

**Methods:**
- `authenticate()` → bool
- `get_fund_limits()` → dict
- `get_ltp(security_id, exchange_segment)` → float
- `get_historical_data(...)` → dict
- `place_order(...)` → dict
- `get_order_status(order_id)` → dict

### utils.instruments.InstrumentManager

```python
from utils.instruments import InstrumentManager

# Initialize
manager = InstrumentManager(dhan_client)

# Load instruments
manager.load_instruments()

# Get nearest expiry
expiry = manager.get_nearest_expiry()  # '2026-01-08'

# Calculate ATM strike
atm = manager.get_atm_strike(23567.50)  # 23550

# Get security ID
sec_id = manager.get_option_security_id(
    expiry='2026-01-08',
    strike=23500,
    option_type='CE'
)
```

**Methods:**
- `download_instruments()` → bool
- `load_instruments()` → bool
- `filter_options(underlying)` → DataFrame
- `get_nearest_expiry()` → str
- `get_atm_strike(index_ltp)` → int
- `get_option_security_id(expiry, strike, option_type)` → int

### utils.market_time.MarketTime

```python
from utils.market_time import MarketTime

# Check if market is open
is_open = MarketTime.is_market_open()

# Get current IST time
now = MarketTime.get_current_time()

# Time to market open
msg = MarketTime.time_to_market_open()
```

**Class Methods:**
- `is_market_open()` → bool
- `get_current_time()` → datetime
- `time_to_market_open()` → str

**Constants:**
- `MARKET_OPEN`: time(9, 15)
- `MARKET_CLOSE`: time(15, 30)
- `IST`: pytz.timezone('Asia/Kolkata')

### strategy.supertrend.SuperTrendStrategy

```python
from strategy.supertrend import SuperTrendStrategy

# Initialize
strategy = SuperTrendStrategy(period=7, multiplier=4)

# Add price data
strategy.add_price_data(
    timestamp=datetime.now(),
    open_price=150.0,
    high=152.0,
    low=148.0,
    close=151.0,
    volume=1000
)

# Calculate SuperTrend
st_data = strategy.calculate_supertrend()
# Returns: {'supertrend': float, 'direction': int, 'close': float}

# Generate signal
signal = strategy.generate_signal()
# Returns: {'type': 'BUY'/'SELL', 'price': float, ...} or None

# Get current trend
trend = strategy.get_current_trend()  # 'UPTREND' or 'DOWNTREND'

# Reset
strategy.reset()
```

**Methods:**
- `add_price_data(timestamp, open, high, low, close, volume)` → None
- `calculate_supertrend()` → dict
- `generate_signal()` → dict or None
- `get_current_trend()` → str
- `reset()` → None

### risk.risk_manager.RiskManager

```python
from risk.risk_manager import RiskManager

# Initialize
risk_mgr = RiskManager()

# Check if can trade
can_trade, reason = risk_mgr.can_place_trade()

# Add position
risk_mgr.add_position(
    position_id='pos_123',
    entry_price=150.0,
    quantity=25,
    option_type='CE'
)

# Update position (check stops)
stop_hit = risk_mgr.update_position('pos_123', 145.0)
# Returns: 'STOP_LOSS', 'TRAILING_STOP', or None

# Close position
result = risk_mgr.close_position('pos_123', 155.0)
# Returns: dict with P&L details

# Kill-switch
risk_mgr.activate_kill_switch()
risk_mgr.deactivate_kill_switch()

# Get summary
summary = risk_mgr.get_daily_summary()
```

**Methods:**
- `can_place_trade()` → (bool, str)
- `add_position(position_id, entry_price, quantity, option_type)` → None
- `update_position(position_id, current_price)` → str or None
- `close_position(position_id, exit_price)` → dict
- `activate_kill_switch()` → None
- `deactivate_kill_switch()` → None
- `get_daily_summary()` → dict

### execution.paper.PaperTrading

```python
from execution.paper import PaperTrading

# Initialize
paper = PaperTrading()

# Place order
result = paper.place_order(
    security_id=123456,
    symbol='NIFTY 2026-01-08 23500 CE',
    price=150.0,
    quantity=25,
    order_type='BUY'
)

# Get positions
positions = paper.get_positions()

# Calculate P&L
pnl = paper.calculate_pnl()
```

**Methods:**
- `place_order(security_id, symbol, price, quantity, order_type)` → dict
- `get_positions()` → dict
- `get_trades()` → list
- `calculate_pnl()` → float

### execution.live.LiveTrading

```python
from execution.live import LiveTrading

# Initialize
live = LiveTrading(dhan_client)

# Place order
result = live.place_order(
    security_id=123456,
    symbol='NIFTY 2026-01-08 23500 CE',
    price=150.0,
    quantity=25,
    transaction_type='BUY'
)

# Get order status
status = live.get_order_status(order_id)

# Enable/disable
live.enable_live_trading()
live.disable_live_trading()
```

**Methods:**
- `place_order(security_id, symbol, price, quantity, transaction_type)` → dict
- `get_order_status(order_id)` → dict
- `enable_live_trading()` → None
- `disable_live_trading()` → None

---

## Strategy Guide

### SuperTrend Indicator

#### What is SuperTrend?

SuperTrend is a trend-following indicator that identifies the market trend direction. It plots a line that acts as support in uptrends and resistance in downtrends.

#### How It Works

1. **Calculate True Range (TR)**
   ```
   TR = max(High - Low, |High - Previous Close|, |Low - Previous Close|)
   ```

2. **Calculate Average True Range (ATR)**
   ```
   ATR = Moving Average of TR over 'period' candles
   ```

3. **Calculate Basic Bands**
   ```
   Basic Upper Band = (High + Low) / 2 + (Multiplier × ATR)
   Basic Lower Band = (High + Low) / 2 - (Multiplier × ATR)
   ```

4. **Calculate Final Bands**
   - Upper band adjusts downward or stays same
   - Lower band adjusts upward or stays same

5. **Determine SuperTrend Line**
   - If Close > Upper Band: SuperTrend = Lower Band (Uptrend)
   - If Close < Upper Band: SuperTrend = Upper Band (Downtrend)

#### Trading Signals

**BUY Signal (Long Entry)**
- Occurs when price crosses ABOVE the SuperTrend line
- Indicates start of uptrend
- Action: Buy call option

**SELL Signal (Long Exit)**
- Occurs when price crosses BELOW the SuperTrend line
- Indicates start of downtrend
- Action: Sell/exit call option

#### Parameters

**Period (Default: 7)**
- Number of candles for ATR calculation
- Lower period = More sensitive, more signals
- Higher period = Less sensitive, fewer signals
- Typical range: 5-21

**Multiplier (Default: 4)**
- Distance of SuperTrend from price
- Lower multiplier = Closer to price, more signals
- Higher multiplier = Further from price, fewer signals
- Typical range: 2-5

#### Parameter Tuning

**For Scalping (1-min candles)**
- Period: 5-7
- Multiplier: 2-3
- Result: Many signals, quick trades

**For Intraday (5-min candles)**
- Period: 7-14
- Multiplier: 3-4
- Result: Moderate signals, balanced

**For Positional (15-min+ candles)**
- Period: 14-21
- Multiplier: 4-5
- Result: Few signals, strong trends

### Strategy Implementation

#### Entry Logic

```python
if signal['type'] == 'BUY' and no_position:
    if can_place_trade():
        place_buy_order()
        add_position()
```

#### Exit Logic

```python
if signal['type'] == 'SELL' and has_position:
    close_position()
    
if stop_loss_hit:
    close_position()
    
if trailing_stop_hit:
    close_position()
```

#### Position Sizing

Current implementation: Fixed lot size

```python
quantity = config.LOT_SIZE * lot_multiplier
# NIFTY: 1 lot = 25 shares
# BANKNIFTY: 1 lot = 15 shares (check current)
```

**Future enhancement**: Dynamic sizing based on capital
```python
capital = get_available_capital()
risk_per_trade = capital * 0.02  # 2% risk
quantity = calculate_quantity(risk_per_trade, stop_loss_distance)
```

### Backtesting Results

*Note: Backtest your strategy with historical data before live trading*

**Recommended Process:**
1. Collect historical data (1-3 months)
2. Run strategy on historical data
3. Calculate metrics:
   - Win rate
   - Average profit per trade
   - Average loss per trade
   - Maximum drawdown
   - Sharpe ratio
4. Optimize parameters
5. Forward test with paper trading
6. Go live with small size

---

## Risk Management

### Multi-Layer Risk Framework

```
Layer 1: Per-Trade Risk
├─ Stop Loss (30%)
└─ Trailing Stop (10%)

Layer 2: Daily Risk
├─ Max Trades (20)
└─ Max Loss (₹20,000)

Layer 3: System Risk
├─ Kill-Switch
└─ Market Hours Check

Layer 4: Operational Risk
├─ Error Handling
└─ Graceful Shutdown
```

### Stop Loss

**Purpose**: Limit loss on each trade

**Mechanism:**
- Set at entry: `stop_price = entry_price × (1 - STOP_LOSS_PERCENT/100)`
- Triggers when: `current_price <= stop_price`
- Action: Close position immediately

**Example:**
```
Entry: ₹100
Stop Loss (30%): ₹70
If price drops to ₹70 → Position closes
Maximum loss: ₹30 per share
```

**Tuning:**
- Tight (15-20%): Less risk, more stop-outs
- Medium (20-30%): Balanced
- Loose (30-40%): More risk, fewer stop-outs

### Trailing Stop Loss

**Purpose**: Lock in profits as price moves favorably

**Mechanism:**
- Tracks highest price since entry
- Updates dynamically: `trailing_stop = highest_price × (1 - TRAILING_PERCENT/100)`
- Triggers when: `current_price <= trailing_stop`
- Action: Close position with profit

**Example:**
```
Entry: ₹100
Price rises to: ₹150
Highest: ₹150
Trailing Stop (10%): ₹135

If price drops to ₹135 → Position closes
Profit: ₹35 per share (35%)
```

**Tuning:**
- Tight (5-8%): Lock profits quickly, may exit early
- Medium (8-12%): Balanced
- Loose (12-15%): Allow more pullback, maximize gains

### Daily Limits

**Max Trades Per Day**
- **Purpose**: Prevent overtrading
- **Mechanism**: Counter incremented on each trade
- **When hit**: No new trades until next day
- **Typical values**: 5-20 trades

**Max Loss Per Day**
- **Purpose**: Protect capital on bad days
- **Mechanism**: Cumulative P&L tracked
- **When hit**: Trading stops, kill-switch activated
- **Typical values**: 2-5% of total capital

### Position Sizing

**Current Approach: Fixed Lot Size**
```python
position_value = option_price × lot_size × lot_multiplier
# Example: ₹150 × 10 lots × 25 shares = ₹37,500
```

**Risk Per Trade:**
```
Maximum Risk = position_value × (STOP_LOSS_PERCENT / 100)
Example: ₹37,500 × 0.30 = ₹11,250
```

**Recommended: Percentage-Based Sizing**
```python
# Risk 2% of capital per trade
capital = 500000  # ₹5 lakh
risk_per_trade = capital * 0.02  # ₹10,000

# Calculate lot size
max_loss_per_lot = (entry_price × STOP_LOSS_PERCENT / 100) × lot_multiplier
lots = risk_per_trade / max_loss_per_lot
```

### Risk Monitoring

**Real-Time Checks:**
- Position count
- Daily P&L
- Available margin
- Open order count

**Daily Summary:**
```python
{
    'date': '2026-01-03',
    'total_trades': 5,
    'daily_pnl': -2500,
    'active_positions': 1,
    'max_trades_limit': 20,
    'max_loss_limit': 20000,
    'kill_switch_active': False
}
```

### Emergency Procedures

**Kill-Switch Activation:**
```python
# Manually activate
risk_manager.activate_kill_switch()

# Automatically activates when:
# - Daily loss limit reached
# - Critical error detected
```

**Recovery:**
```python
# Review logs
tail -f logs/bot_20260103.log

# Check positions
cat data/trades/trades_2026-01-03.json

# Deactivate (next day)
risk_manager.deactivate_kill_switch()
```

---

## Usage Guide

### Basic Usage

#### Starting the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Run
python main.py
```

#### Stopping the Bot

```bash
# Graceful shutdown
Ctrl+C

# Force stop (not recommended)
Ctrl+Z
kill %1
```

#### Running in Background

**Using nohup:**
```bash
nohup python main.py > bot.out 2>&1 &

# Check if running
ps aux | grep main.py

# Stop
kill <PID>
```

**Using screen:**
```bash
# Create session
screen -S trading_bot

# Run bot
python main.py

# Detach: Ctrl+A then D

# Reattach
screen -r trading_bot

# List sessions
screen -ls

# Kill session
screen -X -S trading_bot quit
```

**Using tmux:**
```bash
# Create session
tmux new -s trading_bot

# Run bot
python main.py

# Detach: Ctrl+B then D

# Reattach
tmux attach -t trading_bot

# List sessions
tmux ls

# Kill session
tmux kill-session -t trading_bot
```

### Daily Operations

#### Morning Routine (Before Market Open)

```bash
# 1. Check logs from previous day
tail -100 logs/bot_$(date -d yesterday +%Y%m%d).log

# 2. Review trades
cat data/trades/trades_$(date -d yesterday +%Y-%m-%d).json

# 3. Update .env if needed
nano .env

# 4. Test components
python test_bot.py

# 5. Start bot
python main.py &
```

#### During Market Hours

```bash
# Monitor real-time
tail -f logs/bot_$(date +%Y%m%d).log

# Check positions
grep "Position" logs/bot_$(date +%Y%m%d).log

# Check signals
grep "SIGNAL" logs/bot_$(date +%Y%m%d).log

# Check daily P&L
grep "Daily Summary" logs/bot_$(date +%Y%m%d).log | tail -1
```

#### End of Day

```bash
# 1. Stop bot (if not auto-stopped)
# Ctrl+C or kill process

# 2. Review performance
cat data/trades/trades_$(date +%Y-%m-%d).json

# 3. Calculate P&L
python -c "
import json
with open('data/trades/trades_$(date +%Y-%m-%d).json') as f:
    trades = json.load(f)
    pnl = sum(t.get('pnl', 0) for t in trades)
    wins = [t for t in trades if t.get('pnl', 0) > 0]
    print(f'Trades: {len(trades)}, Wins: {len(wins)}, P&L: ₹{pnl:.2f}')
"

# 4. Backup logs
cp logs/bot_$(date +%Y%m%d).log backups/
```

### Advanced Usage

#### Custom Strategy Parameters

```bash
# Override via environment variables
SUPERTREND_PERIOD=10 SUPERTREND_MULTIPLIER=3 python main.py
```

#### Paper to Live Transition

```bash
# 1. Test paper trading for 2 weeks
TRADING_MODE=paper python main.py

# 2. Review results
ls -lh data/trades/

# 3. Switch to live (start small)
# Edit .env
LOT_SIZE=1
TRADING_MODE=live

# 4. Run with extra monitoring
python main.py 2>&1 | tee live_trading.log
```

#### Multiple Instances

```bash
# Instance 1: NIFTY
INDEX_NAME=NIFTY python main.py &

# Instance 2: BANKNIFTY (future)
# INDEX_NAME=BANKNIFTY python main.py &
```

---

## Deployment

### Production Deployment

#### 1. Server Setup

**Cloud Provider Options:**
- AWS EC2 (t3.small or larger)
- Google Cloud Compute Engine
- DigitalOcean Droplet
- Linode

**Recommended Specs:**
- OS: Ubuntu 22.04 LTS
- CPU: 2 cores
- RAM: 2 GB
- Storage: 20 GB SSD
- Region: Mumbai (for low latency to NSE)

#### 2. Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Create user
sudo useradd -m -s /bin/bash tradingbot
sudo su - tradingbot

# Clone repository
git clone https://github.com/yourusername/index-options-bot.git
cd index-options-bot/index_options_bot

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env
```

#### 3. Systemd Service

Create `/etc/systemd/system/trading-bot.service`:

```ini
[Unit]
Description=Index Options Trading Bot
After=network.target

[Service]
Type=simple
User=tradingbot
WorkingDirectory=/home/tradingbot/index-options-bot/index_options_bot
Environment="PATH=/home/tradingbot/index-options-bot/index_options_bot/venv/bin"
ExecStart=/home/tradingbot/index-options-bot/index_options_bot/venv/bin/python main.py
Restart=on-failure
RestartSec=10
StandardOutput=append:/var/log/trading-bot/stdout.log
StandardError=append:/var/log/trading-bot/stderr.log

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
# Create log directory
sudo mkdir -p /var/log/trading-bot
sudo chown tradingbot:tradingbot /var/log/trading-bot

# Enable service
sudo systemctl enable trading-bot

# Start service
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot

# View logs
sudo journalctl -u trading-bot -f
```

#### 4. Monitoring

**Setup log rotation:**

Create `/etc/logrotate.d/trading-bot`:
```
/home/tradingbot/index-options-bot/index_options_bot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 tradingbot tradingbot
}
```

**Setup alerts (optional):**
```bash
# Install monitoring tools
sudo apt install monit

# Configure monit
# /etc/monit/conf.d/trading-bot
check process trading-bot with pidfile /var/run/trading-bot.pid
    start program = "/bin/systemctl start trading-bot"
    stop program = "/bin/systemctl stop trading-bot"
    if cpu > 80% for 5 cycles then alert
    if totalmem > 500 MB for 5 cycles then alert
```

#### 5. Security

**Firewall:**
```bash
sudo ufw enable
sudo ufw allow 22/tcp  # SSH only
sudo ufw status
```

**Secure .env:**
```bash
chmod 600 .env
```

**Regular updates:**
```bash
# Create update script
cat > update_bot.sh << 'EOF'
#!/bin/bash
cd ~/index-options-bot/index_options_bot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart trading-bot
EOF

chmod +x update_bot.sh
```

#### 6. Backup

**Automated backup script:**
```bash
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=~/backups/$DATE

mkdir -p $BACKUP_DIR

# Backup data
cp -r data/ $BACKUP_DIR/
cp -r logs/ $BACKUP_DIR/
cp .env $BACKUP_DIR/

# Compress
cd ~/backups
tar -czf $DATE.tar.gz $DATE
rm -rf $DATE

# Keep only last 30 days
find ~/backups -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to crontab (daily at midnight)
crontab -e
# Add: 0 0 * * * ~/index-options-bot/index_options_bot/backup.sh
```

### Container Deployment (Docker)

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p data/instruments data/trades data/pnl logs

# Run
CMD ["python", "main.py"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  trading-bot:
    build: .
    container_name: index-options-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### Usage

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

---

## Monitoring & Logs

### Log Files

#### Structure

```
logs/
├── bot_20260103.log
├── bot_20260104.log
└── bot_20260105.log
```

#### Log Levels

- **INFO**: Normal operations
- **WARNING**: Important but not critical
- **ERROR**: Errors that need attention
- **CRITICAL**: Severe errors

#### Log Format

```
2026-01-03 16:48:43,323 - module_name - LEVEL - message
```

### Common Log Patterns

#### Successful Authentication
```
INFO - utils.dhan_client - ✓ Authentication successful
INFO - utils.dhan_client - Available Balance: ₹500000
```

#### Price Updates
```
INFO - __main__ - Index LTP: 23500
INFO - __main__ - Option LTP: ₹149.59
```

#### Signals
```
INFO - strategy.supertrend - 🟢 BUY SIGNAL: Price crossed above SuperTrend at 155.50
INFO - strategy.supertrend - 🔴 SELL SIGNAL: Price crossed below SuperTrend at 145.20
```

#### Trade Execution
```
INFO - execution.paper - 💰 PAPER BUY: NIFTY 2026-01-08 23500 CE @ ₹155.50 x 10
INFO - execution.paper - 💸 PAPER SELL: NIFTY 2026-01-08 23500 CE @ ₹145.20 x 10
```

#### Stop Triggers
```
WARNING - risk.risk_manager - ⚠️ Stop Loss hit: ₹140.50 <= ₹142.00
WARNING - risk.risk_manager - ⚠️ Trailing Stop hit: ₹148.00 <= ₹148.50
```

#### Errors
```
ERROR - utils.dhan_client - Error fetching LTP: Connection timeout
ERROR - __main__ - Error in trading cycle: NoneType object has no attribute 'get'
```

### Log Analysis

#### View Today's Log
```bash
cat logs/bot_$(date +%Y%m%d).log
```

#### Filter by Level
```bash
# Errors only
grep ERROR logs/bot_$(date +%Y%m%d).log

# Warnings and Errors
grep -E "WARNING|ERROR" logs/bot_$(date +%Y%m%d).log
```

#### Count Signals
```bash
# Buy signals
grep "BUY SIGNAL" logs/bot_$(date +%Y%m%d).log | wc -l

# Sell signals
grep "SELL SIGNAL" logs/bot_$(date +%Y%m%d).log | wc -l
```

#### Extract Trades
```bash
# All trades
grep -E "PAPER BUY|PAPER SELL|LIVE ORDER" logs/bot_$(date +%Y%m%d).log
```

#### Monitor Real-Time
```bash
# All logs
tail -f logs/bot_$(date +%Y%m%d).log

# Signals only
tail -f logs/bot_$(date +%Y%m%d).log | grep --line-buffered SIGNAL

# Errors only
tail -f logs/bot_$(date +%Y%m%d).log | grep --line-buffered ERROR
```

### Trade Files

#### JSON Format

```json
[
  {
    "order_id": "PAPER_20260103_164843_100040",
    "security_id": 100040,
    "symbol": "NIFTY 2026-01-08 23500 CE",
    "order_type": "BUY",
    "price": 155.50,
    "quantity": 250,
    "timestamp": "2026-01-03T11:18:43.123456Z",
    "status": "COMPLETED"
  },
  {
    "order_id": "PAPER_20260103_165120_100040",
    "security_id": 100040,
    "symbol": "NIFTY 2026-01-08 23500 CE",
    "order_type": "SELL",
    "price": 145.20,
    "quantity": 250,
    "timestamp": "2026-01-03T11:21:20.654321Z",
    "status": "COMPLETED",
    "pnl": -2575.00
  }
]
```

#### CSV Format

```csv
order_id,security_id,symbol,order_type,price,quantity,timestamp,status,pnl
PAPER_20260103_164843_100040,100040,NIFTY 2026-01-08 23500 CE,BUY,155.50,250,2026-01-03T11:18:43.123456Z,COMPLETED,
PAPER_20260103_165120_100040,100040,NIFTY 2026-01-08 23500 CE,SELL,145.20,250,2026-01-03T11:21:20.654321Z,COMPLETED,-2575.00
```

### Performance Analysis

#### Calculate Daily P&L

```python
import json
from datetime import date

# Load today's trades
with open(f'data/trades/trades_{date.today()}.json') as f:
    trades = json.load(f)

# Calculate metrics
total_trades = len([t for t in trades if t['order_type'] == 'BUY'])
wins = [t for t in trades if t.get('pnl', 0) > 0]
losses = [t for t in trades if t.get('pnl', 0) < 0]

total_pnl = sum(t.get('pnl', 0) for t in trades)
avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0
win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0

print(f"Total Trades: {total_trades}")
print(f"Wins: {len(wins)} ({win_rate:.1f}%)")
print(f"Losses: {len(losses)}")
print(f"Total P&L: ₹{total_pnl:.2f}")
print(f"Avg Win: ₹{avg_win:.2f}")
print(f"Avg Loss: ₹{avg_loss:.2f}")
```

#### Weekly Analysis

```bash
# Create analysis script
python -c "
import json, glob
from datetime import datetime, timedelta

# Get last 7 days of trades
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

all_trades = []
for f in glob.glob('data/trades/trades_*.json'):
    all_trades.extend(json.load(open(f)))

# Filter by date range
trades = [t for t in all_trades 
          if start_date <= datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) <= end_date]

# Calculate
pnl = sum(t.get('pnl', 0) for t in trades)
print(f'Weekly P&L: ₹{pnl:.2f}')
print(f'Trades: {len([t for t in trades if t[\"order_type\"] == \"BUY\"])}')
"
```

---

## Troubleshooting

### Common Issues

#### 1. Authentication Failed

**Symptoms:**
```
ERROR - Authentication failed: Client ID or access token is invalid
```

**Solutions:**
- Verify credentials in `.env` file
- Check if token has expired (regenerate in Dhan portal)
- Ensure API access is enabled in your Dhan account
- Check for extra spaces in `.env` file

#### 2. No Valid Expiry Found

**Symptoms:**
```
ERROR - No valid future expiries found
```

**Solutions:**
- Delete cached instruments: `rm data/instruments/nfo_instruments.csv`
- Restart bot (will re-download)
- Check if it's a trading holiday
- Verify instrument data source

#### 3. Bot Not Generating Signals

**Symptoms:**
- Bot runs but no buy/sell signals appear

**Solutions:**
- Check if enough candles collected (need >= SUPERTREND_PERIOD)
- Verify market is open
- Check price data is being collected: `grep "Option LTP" logs/bot_*.log`
- Review strategy parameters (may need tuning)

#### 4. Import Errors

**Symptoms:**
```
ImportError: No module named 'dhanhq'
```

**Solutions:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check installation
pip list | grep dhanhq
```

#### 5. Permission Denied

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'data/trades/trades_2026-01-03.json'
```

**Solutions:**
```bash
# Fix permissions
chmod -R 755 data/
chmod -R 755 logs/

# Or change ownership
sudo chown -R $USER:$USER .
```

#### 6. Market Closed

**Symptoms:**
```
WARNING - Market is CLOSED. 17h 26m until market opens
```

**Solutions:**
- This is normal outside trading hours
- Bot continues in demo mode with simulated data
- Wait for market hours: 9:15 AM - 3:30 PM IST (Mon-Fri)

#### 7. Connection Timeout

**Symptoms:**
```
ERROR - Error fetching LTP: Connection timeout
```

**Solutions:**
- Check internet connection
- Verify Dhan API is accessible: `ping api.dhan.co`
- Check firewall settings
- Try increasing timeout in code

#### 8. Disk Space Full

**Symptoms:**
```
OSError: [Errno 28] No space left on device
```

**Solutions:**
```bash
# Check disk usage
df -h

# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete

# Clean old trades (backup first!)
find data/trades/ -name "*.json" -mtime +90 -delete
```

### Debugging

#### Enable Debug Logging

Edit `main.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
```

#### Test Components Individually

```bash
# Test configuration
python -c "from config.settings import config; config.validate(); print('OK')"

# Test Dhan authentication
python -c "from utils.dhan_client import DhanClient; c=DhanClient(); print(c.authenticate())"

# Test SuperTrend
python test_bot.py
```

#### Check Process

```bash
# Find running instance
ps aux | grep main.py

# Check resource usage
top -p <PID>

# Check open files
lsof -p <PID>
```

### Error Recovery

#### Corrupted Data Files

```bash
# Backup current
cp data/trades/trades_2026-01-03.json data/trades/trades_2026-01-03.json.bak

# Try to repair JSON
python -c "
import json
with open('data/trades/trades_2026-01-03.json') as f:
    try:
        data = json.load(f)
        print('JSON is valid')
    except json.JSONDecodeError as e:
        print(f'JSON error: {e}')
"
```

#### Reset State

```bash
# Backup everything
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/

# Clean data (WARNING: deletes all data)
rm -rf data/trades/*
rm -rf data/instruments/*
rm -rf logs/*

# Restart fresh
python main.py
```

### Getting Help

1. **Check logs first**: `tail -100 logs/bot_$(date +%Y%m%d).log`
2. **Run tests**: `python test_bot.py`
3. **Check configuration**: `cat .env`
4. **Review recent changes**: `git log -5` (if using git)
5. **Search documentation**: Ctrl+F in this file

---

## Performance Optimization

### Bot Performance

#### Reduce Latency

**1. Use low-latency server**
- Host in Mumbai region (close to NSE)
- Use dedicated server (not shared hosting)

**2. Optimize polling interval**
```bash
# Current: 1 second
POLLING_INTERVAL=1

# For faster execution (more API calls)
POLLING_INTERVAL=0.5

# For slower (fewer API calls)
POLLING_INTERVAL=5
```

**3. Use WebSocket (future enhancement)**
- Real-time price updates instead of polling
- Lower latency
- Fewer API calls

#### Optimize Memory

**Current usage:** ~50-100 MB

**To reduce:**
- Limit price_data history in strategy
- Archive old logs regularly
- Compress trade files

```python
# In supertrend.py
# Keep only last 100 candles
if len(self.price_data) > 100:
    self.price_data = self.price_data[-100:]
```

#### Optimize Disk I/O

**Batch writes:**
```python
# Instead of writing on every trade
# Buffer and write every N trades or every M seconds
```

**Use SSD:**
- Faster read/write
- Better for frequent logging

### Strategy Performance

#### Parameter Optimization

**Brute Force Approach:**
```python
# Test different combinations
periods = [5, 7, 10, 14]
multipliers = [2, 3, 4, 5]

for period in periods:
    for multiplier in multipliers:
        # Run backtest
        # Calculate metrics
        # Compare results
```

**Grid Search:**
```python
from itertools import product

params = {
    'period': range(5, 21),
    'multiplier': [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
    'timeframe': [1, 3, 5]
}

best_params = None
best_sharpe = -999

for combo in product(*params.values()):
    # Test combination
    # Calculate Sharpe ratio
    # Update best if better
```

#### Walk-Forward Optimization

1. Split data: In-sample (training) + Out-of-sample (testing)
2. Optimize on in-sample
3. Test on out-of-sample
4. Roll forward, repeat

### Execution Performance

#### Order Execution

**Market Orders (Current):**
- Pros: Fast execution
- Cons: Slippage risk

**Limit Orders (Future):**
- Pros: Price control
- Cons: May not fill

**Smart Order Routing:**
```python
# Check spread
if spread < threshold:
    place_market_order()
else:
    place_limit_order(mid_price)
```

### Monitoring Performance

#### Key Metrics

```python
metrics = {
    'win_rate': wins / total_trades,
    'profit_factor': total_profit / abs(total_loss),
    'avg_win': total_profit / wins,
    'avg_loss': total_loss / losses,
    'sharpe_ratio': calculate_sharpe(returns),
    'max_drawdown': calculate_max_drawdown(equity_curve),
    'trades_per_day': total_trades / trading_days
}
```

#### Performance Dashboard (Future)

Create `performance.py`:
```python
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load all trades
trades = load_all_trades()

# Calculate equity curve
equity = calculate_equity_curve(trades)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(equity)
plt.title('Equity Curve')
plt.xlabel('Trade Number')
plt.ylabel('Equity (₹)')
plt.grid(True)
plt.savefig('equity_curve.png')
```

---

## Security Best Practices

### Credential Management

#### Never Hardcode Credentials

❌ **Bad:**
```python
client_id = "1234567890"
access_token = "abcdefghijklmnopqrstuvwxyz"
```

✅ **Good:**
```python
client_id = os.getenv('DHAN_CLIENT_ID')
access_token = os.getenv('DHAN_ACCESS_TOKEN')
```

#### Protect .env File

```bash
# Set restrictive permissions
chmod 600 .env

# Never commit to git
echo ".env" >> .gitignore

# Use .env.example for templates
cp .env .env.example
# Remove sensitive values from .env.example
```

#### Rotate Credentials Regularly

- Change Dhan API tokens every 3-6 months
- Generate new tokens if compromised
- Use different tokens for different environments

### Server Security

#### Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow only SSH
sudo ufw allow 22/tcp

# Block all other incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Check status
sudo ufw status verbose
```

#### SSH Hardening

```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no (use key-based auth)

# Restart SSH
sudo systemctl restart sshd
```

#### Regular Updates

```bash
# Setup unattended upgrades
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

### Application Security

#### Input Validation

```python
# Validate configuration
def validate():
    if not DHAN_CLIENT_ID or len(DHAN_CLIENT_ID) < 5:
        raise ValueError("Invalid DHAN_CLIENT_ID")
    
    if TRADING_MODE not in ['paper', 'live']:
        raise ValueError("TRADING_MODE must be 'paper' or 'live'")
    
    if LOT_SIZE < 1 or LOT_SIZE > 100:
        raise ValueError("LOT_SIZE must be between 1 and 100")
```

#### Error Handling

```python
# Don't expose sensitive info in errors
try:
    client.authenticate()
except Exception as e:
    # ❌ Don't log full exception (may contain credentials)
    # logger.error(f"Auth failed: {e}")
    
    # ✅ Log generic message
    logger.error("Authentication failed. Check credentials.")
```

#### Rate Limiting

```python
# Prevent API abuse
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
    
    def allow_request(self):
        now = time.time()
        # Remove old calls
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
```

### Data Security

#### Encrypt Sensitive Data

```python
# For future: encrypt trade data at rest
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(data.encode())

# Decrypt
decrypted = cipher.decrypt(encrypted).decode()
```

#### Backup Encryption

```bash
# Encrypt backups
tar -czf - data/ | gpg --symmetric --cipher-algo AES256 -o backup.tar.gz.gpg

# Decrypt
gpg --decrypt backup.tar.gz.gpg | tar -xzf -
```

### Monitoring & Alerts

#### Failed Login Attempts

```python
# Track failed auth attempts
failed_auth_count = 0
MAX_FAILED_AUTH = 5

if not authenticate():
    failed_auth_count += 1
    if failed_auth_count >= MAX_FAILED_AUTH:
        logger.critical("Multiple auth failures - possible attack")
        send_alert()
```

#### Unusual Activity

```python
# Detect unusual trading patterns
if daily_trades > MAX_TRADES_PER_DAY * 2:
    logger.warning("Unusual trade volume detected")
    activate_kill_switch()
```

---

## API Reference

### Dhan API Endpoints

#### Authentication

```python
# Already handled in DhanClient
client = DhanClient()
client.authenticate()
```

#### Get Fund Limits

```python
funds = client.get_fund_limits()
# Returns:
# {
#     'status': 'success',
#     'data': {
#         'availabelBalance': 500000.00,
#         'collateralAmount': 0,
#         'utilizedAmount': 50000.00
#     }
# }
```

#### Get LTP

```python
ltp = client.get_ltp(
    security_id='52175',  # NIFTY index
    exchange_segment='IDX_I'
)
# Returns: 23567.50
```

#### Place Order

```python
response = client.place_order(
    security_id='123456',
    exchange_segment='NSE_FNO',
    transaction_type='BUY',  # or 'SELL'
    quantity=25,
    order_type='MARKET',  # or 'LIMIT', 'STOP_LOSS'
    product_type='INTRADAY',  # or 'CNC', 'MTF'
    price=0  # 0 for market orders
)
# Returns:
# {
#     'status': 'success',
#     'data': {
#         'orderId': '123456789'
#     }
# }
```

#### Get Order Status

```python
status = client.get_order_status('123456789')
# Returns:
# {
#     'status': 'success',
#     'data': {
#         'orderId': '123456789',
#         'orderStatus': 'TRADED',
#         'transactionType': 'BUY',
#         'tradedPrice': 150.50,
#         'tradedQuantity': 25
#     }
# }
```

### Exchange Segments

```python
EXCHANGE_SEGMENTS = {
    'NSE_EQ': 'NSE Equity',
    'NSE_FNO': 'NSE Futures & Options',
    'BSE_EQ': 'BSE Equity',
    'BSE_FNO': 'BSE Futures & Options',
    'MCX_COMM': 'MCX Commodity',
    'IDX_I': 'Index'
}
```

### Order Types

```python
ORDER_TYPES = {
    'MARKET': 'Market Order',
    'LIMIT': 'Limit Order',
    'STOP_LOSS': 'Stop Loss Order',
    'STOP_LOSS_MARKET': 'Stop Loss Market Order'
}
```

### Product Types

```python
PRODUCT_TYPES = {
    'INTRADAY': 'Intraday (MIS)',
    'CNC': 'Cash & Carry (Delivery)',
    'MTF': 'Margin Trading Facility',
    'CO': 'Cover Order',
    'BO': 'Bracket Order'
}
```

---

## FAQ

### General Questions

**Q: Is this bot free to use?**
A: Yes, the bot software is free (MIT license). You only pay brokerage fees to Dhan for executed trades.

**Q: Do I need coding knowledge?**
A: Basic command-line knowledge is sufficient. Configuration is done via .env file.

**Q: Can I run multiple bots?**
A: Yes, you can run multiple instances with different configurations.

**Q: Is paper trading really free?**
A: Yes, paper trading is completely simulated. No real money or API calls to broker.

### Trading Questions

**Q: Which options does it trade?**
A: Currently NIFTY index options. Future versions may support BANKNIFTY, FINNIFTY.

**Q: How does it select strikes?**
A: Automatically calculates ATM (At-The-Money) strike based on current index price.

**Q: Which expiry does it use?**
A: Nearest weekly expiry by default. Automatically rolls to next expiry.

**Q: Can it trade multiple positions?**
A: Currently supports one position at a time for safety. Future versions may support multiple.

**Q: Does it support shorting (selling options)?**
A: Current version only buys call options. Future versions may support selling.

### Technical Questions

**Q: What Python version is required?**
A: Python 3.11 or higher.

**Q: Can I run on Windows?**
A: Yes, but Linux is recommended for production.

**Q: Does it use WebSocket for real-time data?**
A: Not currently. Uses polling (HTTP requests at fixed intervals).

**Q: Can I backtest strategies?**
A: Manual backtesting is possible with historical data. Automated backtesting framework is a future enhancement.

**Q: How do I add new strategies?**
A: Create a new strategy file in `strategy/` folder following the same pattern as `supertrend.py`.

### Risk Questions

**Q: How much capital do I need?**
A: Minimum ₹50,000 recommended. Start with paper trading to understand the bot.

**Q: What's the maximum loss per day?**
A: Configurable via MAX_LOSS_PER_DAY in .env (default: ₹20,000).

**Q: Can I lose more than my stop loss?**
A: In extreme market conditions (gap down), you may experience slippage. Use appropriate position sizing.

**Q: What happens if my internet disconnects?**
A: Bot will attempt to reconnect. Use a reliable connection and consider a UPS.

**Q: What if the bot crashes during a trade?**
A: Position tracking is saved to disk. Restart the bot and it will resume. Monitor your Dhan account for open positions.

### Troubleshooting Questions

**Q: Bot says "Authentication failed". What to do?**
A: Check your Dhan credentials in .env file. Ensure API access is enabled in Dhan account.

**Q: No trading signals generated. Why?**
A: Bot needs at least SUPERTREND_PERIOD candles before generating signals. Wait a few minutes.

**Q: Bot stopped trading automatically. Why?**
A: Check if daily limits (MAX_TRADES_PER_DAY or MAX_LOSS_PER_DAY) were hit. Check logs for details.

**Q: How do I reset everything?**
A: Backup data, then delete files in data/ and logs/ folders. Restart bot.

---

## Changelog

### Version 1.0.0 (2026-01-03)

**Initial Release**

**Core Features:**
- SuperTrend strategy implementation
- Paper trading engine
- Live trading engine (toggle)
- Risk management system
- Dhan API integration
- Comprehensive logging
- Trade storage (CSV + JSON)

**Components:**
- Configuration management
- Instrument manager
- Market time utilities
- Multiple execution modes
- Signal generation
- Position tracking

**Documentation:**
- Complete user guide
- API reference
- Troubleshooting guide
- Security best practices

**Known Issues:**
- No WebSocket support (uses polling)
- Single position at a time only
- NIFTY only (no other indices)
- No backtesting framework
- No UI/dashboard

**Future Enhancements:**
- WebSocket for real-time data
- Multiple index support
- Backtesting framework
- Web dashboard
- ML-based strategies
- Database storage
- Alert notifications

---

## Support & Contributing

### Getting Support

1. **Read this documentation thoroughly**
2. **Check troubleshooting section**
3. **Review logs for error messages**
4. **Run test_bot.py for diagnostics**

### Reporting Issues

When reporting issues, include:
- Bot version
- Operating system
- Python version
- Error message (from logs)
- Steps to reproduce
- Configuration (sanitize credentials)

### Contributing

Contributions welcome! Areas for contribution:
- New trading strategies
- Performance optimizations
- Bug fixes
- Documentation improvements
- Test coverage
- UI/Dashboard

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Disclaimer

**IMPORTANT: READ CAREFULLY**

This trading bot is provided for educational and research purposes only. Trading in financial markets involves substantial risk of loss and is not suitable for every investor.

**Key Disclaimers:**

1. **No Guarantees**: Past performance does not guarantee future results. The bot's performance may vary significantly based on market conditions.

2. **Risk of Loss**: You may lose some or all of your invested capital. Never invest money you cannot afford to lose.

3. **No Financial Advice**: This bot does not provide investment advice. Consult a qualified financial advisor before trading.

4. **No Warranty**: The software is provided "as is" without warranty of any kind. The developers are not liable for any losses incurred.

5. **Test Thoroughly**: Always test in paper trading mode extensively before using real money.

6. **Monitor Actively**: Algorithmic trading requires active monitoring. Do not leave the bot unattended for extended periods.

7. **Regulatory Compliance**: Ensure your trading activities comply with local regulations and tax laws.

8. **Broker Relationship**: The bot uses Dhan's API. The developers are not affiliated with Dhan and are not responsible for any broker-related issues.

**By using this bot, you acknowledge that you have read this disclaimer and agree to use the software at your own risk.**

---

**Document Version:** 1.0.0  
**Last Updated:** January 3, 2026  
**Total Pages:** ~75 pages (estimated when printed)

---

*End of Complete Documentation*
