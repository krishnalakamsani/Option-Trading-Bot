import pandas as pd
import numpy as np
import pandas_ta as ta
import logging
from datetime import datetime, timedelta
from config.settings import config

logger = logging.getLogger(__name__)

class SuperTrendStrategy:
    """SuperTrend-based trading strategy for options"""
    
    def __init__(self, period=7, multiplier=4):
        self.period = period
        self.multiplier = multiplier
        self.price_data = []
        self.signals = []
        self.current_trend = None
        
    def add_price_data(self, timestamp, open_price, high, low, close, volume=0):
        """Add new price candle to the dataset"""
        self.price_data.append({
            'timestamp': timestamp,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
        
        # Keep only last 100 candles for efficiency
        if len(self.price_data) > 100:
            self.price_data = self.price_data[-100:]
    
    def calculate_supertrend(self):
        """Calculate SuperTrend indicator"""
        if len(self.price_data) < self.period:
            logger.warning(f"Not enough data for SuperTrend calculation. Need {self.period}, have {len(self.price_data)}")
            return None
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(self.price_data)
            
            # Calculate SuperTrend using pandas_ta
            supertrend = ta.supertrend(
                high=df['high'],
                low=df['low'],
                close=df['close'],
                length=self.period,
                multiplier=self.multiplier
            )
            
            # Get the latest values
            df = pd.concat([df, supertrend], axis=1)
            latest = df.iloc[-1]
            
            # SuperTrend columns: SUPERTd_period_multiplier, SUPERTl_period_multiplier, SUPERTs_period_multiplier
            st_col = f'SUPERT_{self.period}_{self.multiplier}'
            direction_col = f'SUPERTd_{self.period}_{self.multiplier}'
            
            if st_col in df.columns and direction_col in df.columns:
                supertrend_value = latest[st_col]
                direction = latest[direction_col]  # 1 = uptrend, -1 = downtrend
                
                return {
                    'supertrend': supertrend_value,
                    'direction': direction,
                    'close': latest['close'],
                    'timestamp': latest['timestamp']
                }
            else:
                logger.error(f"SuperTrend columns not found in dataframe")
                return None
                
        except Exception as e:
            logger.error(f"Error calculating SuperTrend: {str(e)}")
            return None
    
    def generate_signal(self):
        """Generate trading signal based on SuperTrend"""
        st_data = self.calculate_supertrend()
        
        if st_data is None:
            return None
        
        direction = st_data['direction']
        close = st_data['close']
        supertrend = st_data['supertrend']
        
        signal = None
        
        # Check for trend change
        if self.current_trend is None:
            self.current_trend = direction
            logger.info(f"Initial trend set: {'UPTREND' if direction == 1 else 'DOWNTREND'}")
        
        elif self.current_trend != direction:
            # Trend changed
            if direction == 1:
                # Changed to uptrend - BUY signal
                signal = {
                    'type': 'BUY',
                    'timestamp': st_data['timestamp'],
                    'price': close,
                    'supertrend': supertrend,
                    'reason': 'SuperTrend changed to UPTREND'
                }
                logger.info(f"🟢 BUY SIGNAL: Price crossed above SuperTrend at {close}")
            else:
                # Changed to downtrend - SELL signal
                signal = {
                    'type': 'SELL',
                    'timestamp': st_data['timestamp'],
                    'price': close,
                    'supertrend': supertrend,
                    'reason': 'SuperTrend changed to DOWNTREND'
                }
                logger.info(f"🔴 SELL SIGNAL: Price crossed below SuperTrend at {close}")
            
            self.current_trend = direction
            self.signals.append(signal)
        
        return signal
    
    def get_current_trend(self):
        """Get current market trend"""
        if self.current_trend is None:
            return "UNKNOWN"
        return "UPTREND" if self.current_trend == 1 else "DOWNTREND"
    
    def reset(self):
        """Reset strategy state"""
        self.price_data = []
        self.signals = []
        self.current_trend = None
        logger.info("Strategy reset")