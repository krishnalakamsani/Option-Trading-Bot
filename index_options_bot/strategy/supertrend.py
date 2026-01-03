import pandas as pd
import numpy as np
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
            
            # Calculate True Range (TR)
            df['h-l'] = df['high'] - df['low']
            df['h-pc'] = abs(df['high'] - df['close'].shift(1))
            df['l-pc'] = abs(df['low'] - df['close'].shift(1))
            df['tr'] = df[['h-l', 'h-pc', 'l-pc']].max(axis=1)
            
            # Calculate ATR (Average True Range)
            df['atr'] = df['tr'].rolling(window=self.period).mean()
            
            # Calculate basic bands
            df['basic_ub'] = (df['high'] + df['low']) / 2 + (self.multiplier * df['atr'])
            df['basic_lb'] = (df['high'] + df['low']) / 2 - (self.multiplier * df['atr'])
            
            # Calculate final bands
            df['final_ub'] = 0.0
            df['final_lb'] = 0.0
            
            for i in range(self.period, len(df)):
                # Upper Band
                if df['basic_ub'].iloc[i] < df['final_ub'].iloc[i-1] or df['close'].iloc[i-1] > df['final_ub'].iloc[i-1]:
                    df.loc[df.index[i], 'final_ub'] = df['basic_ub'].iloc[i]
                else:
                    df.loc[df.index[i], 'final_ub'] = df['final_ub'].iloc[i-1]
                
                # Lower Band
                if df['basic_lb'].iloc[i] > df['final_lb'].iloc[i-1] or df['close'].iloc[i-1] < df['final_lb'].iloc[i-1]:
                    df.loc[df.index[i], 'final_lb'] = df['basic_lb'].iloc[i]
                else:
                    df.loc[df.index[i], 'final_lb'] = df['final_lb'].iloc[i-1]
            
            # Calculate SuperTrend
            df['supertrend'] = 0.0
            df['direction'] = 0
            
            for i in range(self.period, len(df)):
                if df['close'].iloc[i] <= df['final_ub'].iloc[i]:
                    df.loc[df.index[i], 'supertrend'] = df['final_ub'].iloc[i]
                    df.loc[df.index[i], 'direction'] = -1  # Downtrend
                else:
                    df.loc[df.index[i], 'supertrend'] = df['final_lb'].iloc[i]
                    df.loc[df.index[i], 'direction'] = 1  # Uptrend
            
            # Get the latest values
            latest = df.iloc[-1]
            
            return {
                'supertrend': latest['supertrend'],
                'direction': latest['direction'],
                'close': latest['close'],
                'timestamp': latest['timestamp']
            }
                
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