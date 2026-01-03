from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
import subprocess
import signal
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Bot process management
bot_process = None
bot_status = {
    "running": False,
    "pid": None,
    "started_at": None,
    "error": None
}

BOT_DIR = Path("/app/index_options_bot")

# Models
class BotConfig(BaseModel):
    dhan_client_id: str
    dhan_access_token: str
    trading_mode: str
    index_name: str
    lot_size: int
    stop_loss_percent: float
    trailing_stop_percent: float
    max_trades_per_day: int
    max_loss_per_day: float
    supertrend_period: int
    supertrend_multiplier: float
    candle_timeframe: int
    polling_interval: int
    strike_interval: int

class BotStatus(BaseModel):
    running: bool
    pid: Optional[int]
    started_at: Optional[str]
    error: Optional[str]

class Trade(BaseModel):
    order_id: str
    security_id: int
    symbol: str
    order_type: str
    price: float
    quantity: int
    timestamp: str
    status: str
    pnl: Optional[float] = None

# Helper functions
def load_bot_config():
    """Load bot configuration from .env file"""
    env_file = BOT_DIR / ".env"
    if not env_file.exists():
        return None
    
    config = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    
    return BotConfig(
        dhan_client_id=config.get('DHAN_CLIENT_ID', ''),
        dhan_access_token=config.get('DHAN_ACCESS_TOKEN', ''),
        trading_mode=config.get('TRADING_MODE', 'paper'),
        index_name=config.get('INDEX_NAME', 'NIFTY'),
        lot_size=int(config.get('LOT_SIZE', 10)),
        stop_loss_percent=float(config.get('STOP_LOSS_PERCENT', 30)),
        trailing_stop_percent=float(config.get('TRAILING_STOP_PERCENT', 10)),
        max_trades_per_day=int(config.get('MAX_TRADES_PER_DAY', 20)),
        max_loss_per_day=float(config.get('MAX_LOSS_PER_DAY', 20000)),
        supertrend_period=int(config.get('SUPERTREND_PERIOD', 7)),
        supertrend_multiplier=float(config.get('SUPERTREND_MULTIPLIER', 4)),
        candle_timeframe=int(config.get('CANDLE_TIMEFRAME', 1)),
        polling_interval=int(config.get('POLLING_INTERVAL', 1)),
        strike_interval=int(config.get('STRIKE_INTERVAL', 50))
    )

def save_bot_config(config: BotConfig):
    """Save bot configuration to .env file"""
    env_file = BOT_DIR / ".env"
    
    env_content = f"""# Dhan API Credentials
DHAN_CLIENT_ID={config.dhan_client_id}
DHAN_ACCESS_TOKEN={config.dhan_access_token}

# Trading Configuration
TRADING_MODE={config.trading_mode}
INDEX_NAME={config.index_name}
LOT_SIZE={config.lot_size}

# Risk Management
STOP_LOSS_PERCENT={config.stop_loss_percent}
TRAILING_STOP_PERCENT={config.trailing_stop_percent}
MAX_TRADES_PER_DAY={config.max_trades_per_day}
MAX_LOSS_PER_DAY={config.max_loss_per_day}

# SuperTrend Strategy
SUPERTREND_PERIOD={config.supertrend_period}
SUPERTREND_MULTIPLIER={config.supertrend_multiplier}
CANDLE_TIMEFRAME={config.candle_timeframe}

# Polling Settings
POLLING_INTERVAL={config.polling_interval}

# Market Settings
STRIKE_INTERVAL={config.strike_interval}
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)

def get_today_trades():
    """Get today's trades from file"""
    today = datetime.now().strftime('%Y-%m-%d')
    trades_file = BOT_DIR / "data" / "trades" / f"trades_{today}.json"
    
    if not trades_file.exists():
        return []
    
    try:
        with open(trades_file, 'r') as f:
            return json.load(f)
    except:
        return []

def get_bot_logs(lines=100):
    """Get bot logs"""
    today = datetime.now().strftime('%Y%m%d')
    log_file = BOT_DIR / "logs" / f"bot_{today}.log"
    
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
    except:
        return []

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Trading Bot API", "version": "1.0.0"}

@api_router.get("/bot/config")
async def get_config():
    """Get current bot configuration"""
    config = load_bot_config()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Mask sensitive data
    config_dict = config.model_dump()
    if config_dict['dhan_access_token']:
        config_dict['dhan_access_token'] = config_dict['dhan_access_token'][:10] + '...' + config_dict['dhan_access_token'][-5:]
    
    return config_dict

@api_router.post("/bot/config")
async def update_config(config: BotConfig):
    """Update bot configuration"""
    try:
        save_bot_config(config)
        return {"status": "success", "message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/status")
async def get_status():
    """Get bot status"""
    global bot_status
    
    # Check if process is still running
    if bot_status["running"] and bot_status["pid"]:
        try:
            os.kill(bot_status["pid"], 0)
        except OSError:
            bot_status["running"] = False
            bot_status["pid"] = None
    
    # Get today's stats
    trades = get_today_trades()
    total_pnl = sum(t.get('pnl', 0) for t in trades)
    total_trades = len([t for t in trades if t.get('order_type') == 'BUY'])
    
    return {
        **bot_status,
        "total_trades_today": total_trades,
        "pnl_today": total_pnl
    }

@api_router.post("/bot/start")
async def start_bot(background_tasks: BackgroundTasks):
    """Start the trading bot"""
    global bot_process, bot_status
    
    if bot_status["running"]:
        return {"status": "already_running", "message": "Bot is already running"}
    
    try:
        # Start bot process
        bot_process = subprocess.Popen(
            ["python", "main.py"],
            cwd=str(BOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        
        bot_status = {
            "running": True,
            "pid": bot_process.pid,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "error": None
        }
        
        return {"status": "success", "message": "Bot started successfully", "pid": bot_process.pid}
    except Exception as e:
        bot_status["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/bot/stop")
async def stop_bot():
    """Stop the trading bot"""
    global bot_process, bot_status
    
    if not bot_status["running"]:
        return {"status": "not_running", "message": "Bot is not running"}
    
    try:
        if bot_status["pid"]:
            os.killpg(os.getpgid(bot_status["pid"]), signal.SIGTERM)
        
        bot_status = {
            "running": False,
            "pid": None,
            "started_at": None,
            "error": None
        }
        
        return {"status": "success", "message": "Bot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/trades")
async def get_trades():
    """Get today's trades"""
    trades = get_today_trades()
    return {"trades": trades, "count": len(trades)}

@api_router.get("/bot/logs")
async def get_logs(lines: int = 100):
    """Get bot logs"""
    logs = get_bot_logs(lines)
    return {"logs": logs, "count": len(logs)}

@api_router.get("/bot/performance")
async def get_performance():
    """Get performance metrics"""
    trades = get_today_trades()
    
    if not trades:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_win": 0,
            "avg_loss": 0
        }
    
    buy_trades = [t for t in trades if t.get('order_type') == 'BUY']
    wins = [t for t in trades if t.get('pnl', 0) > 0]
    losses = [t for t in trades if t.get('pnl', 0) < 0]
    
    total_pnl = sum(t.get('pnl', 0) for t in trades)
    avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
    avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0
    win_rate = len(wins) / len(buy_trades) * 100 if buy_trades else 0
    
    return {
        "total_trades": len(buy_trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2)
    }

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    
    # Stop bot if running
    if bot_status["running"] and bot_status["pid"]:
        try:
            os.killpg(os.getpgid(bot_status["pid"]), signal.SIGTERM)
        except:
            pass