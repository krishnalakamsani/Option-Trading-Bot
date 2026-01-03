import logging
from datetime import datetime, time
import pytz

logger = logging.getLogger(__name__)

class MarketTime:
    """Utilities for market timing"""
    
    IST = pytz.timezone('Asia/Kolkata')
    MARKET_OPEN = time(9, 15)
    MARKET_CLOSE = time(15, 30)
    
    @classmethod
    def is_market_open(cls):
        """Check if market is currently open"""
        now = datetime.now(cls.IST)
        current_time = now.time()
        
        # Check if weekday (Monday=0, Sunday=6)
        if now.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Check if within market hours
        if cls.MARKET_OPEN <= current_time <= cls.MARKET_CLOSE:
            return True
        
        return False
    
    @classmethod
    def get_current_time(cls):
        """Get current IST time"""
        return datetime.now(cls.IST)
    
    @classmethod
    def time_to_market_open(cls):
        """Get time remaining until market opens"""
        now = datetime.now(cls.IST)
        
        if cls.is_market_open():
            return "Market is currently open"
        
        # Calculate next market open
        market_open_today = now.replace(
            hour=cls.MARKET_OPEN.hour,
            minute=cls.MARKET_OPEN.minute,
            second=0,
            microsecond=0
        )
        
        if now.time() > cls.MARKET_CLOSE:
            # Market closed for today, check tomorrow
            from datetime import timedelta
            market_open_today += timedelta(days=1)
        
        # Skip weekends
        while market_open_today.weekday() >= 5:
            from datetime import timedelta
            market_open_today += timedelta(days=1)
        
        time_diff = market_open_today - now
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)
        
        return f"{hours}h {minutes}m until market opens"