import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    # Dhan API
    DHAN_CLIENT_ID = os.getenv('DHAN_CLIENT_ID')
    DHAN_ACCESS_TOKEN = os.getenv('DHAN_ACCESS_TOKEN')
    
    # Trading Mode
    TRADING_MODE = os.getenv('TRADING_MODE', 'paper')  # paper or live
    
    # Index Configuration
    INDEX_NAME = os.getenv('INDEX_NAME', 'NIFTY')
    LOT_SIZE = int(os.getenv('LOT_SIZE', 10))
    STRIKE_INTERVAL = int(os.getenv('STRIKE_INTERVAL', 50))
    
    # Risk Management
    STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', 30))
    TRAILING_STOP_PERCENT = float(os.getenv('TRAILING_STOP_PERCENT', 10))
    MAX_TRADES_PER_DAY = int(os.getenv('MAX_TRADES_PER_DAY', 20))
    MAX_LOSS_PER_DAY = float(os.getenv('MAX_LOSS_PER_DAY', 20000))
    
    # SuperTrend Strategy
    SUPERTREND_PERIOD = int(os.getenv('SUPERTREND_PERIOD', 7))
    SUPERTREND_MULTIPLIER = float(os.getenv('SUPERTREND_MULTIPLIER', 4))
    CANDLE_TIMEFRAME = int(os.getenv('CANDLE_TIMEFRAME', 1))  # in minutes
    
    # Polling
    POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', 1))  # in seconds
    
    # Directories
    DATA_DIR = BASE_DIR / 'data'
    INSTRUMENTS_DIR = DATA_DIR / 'instruments'
    TRADES_DIR = DATA_DIR / 'trades'
    PNL_DIR = DATA_DIR / 'pnl'
    LOGS_DIR = BASE_DIR / 'logs'
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.DHAN_CLIENT_ID or not cls.DHAN_ACCESS_TOKEN:
            raise ValueError("Dhan credentials not found in .env file")
        
        if cls.TRADING_MODE not in ['paper', 'live']:
            raise ValueError("TRADING_MODE must be 'paper' or 'live'")
        
        return True

config = Config()