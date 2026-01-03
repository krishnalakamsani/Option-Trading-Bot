import pandas as pd
import logging
from datetime import datetime, timedelta
from pathlib import Path
from config.settings import config

logger = logging.getLogger(__name__)

class InstrumentManager:
    """Manage instrument data for options trading"""
    
    def __init__(self, dhan_client):
        self.dhan_client = dhan_client
        self.instruments_df = None
        self.instruments_file = config.INSTRUMENTS_DIR / 'nfo_instruments.csv'
        
        # Create instruments directory if it doesn't exist
        config.INSTRUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    def download_instruments(self):
        """Download NFO instrument master from Dhan API"""
        try:
            logger.info("Downloading NFO instruments...")
            
            # Dhan provides instrument data via API or downloadable CSV
            # For now, we'll create a simulated version since we need offline capability
            # In production, use: instruments = self.dhan_client.client.get_scrip_master('NFO')
            
            logger.warning("Using simulated instrument data for demo purposes")
            logger.info("In production, download from: https://api.dhan.co/margincalculator/scrips/NFO")
            
            # Create sample data structure
            sample_data = self._create_sample_instruments()
            self.instruments_df = pd.DataFrame(sample_data)
            
            # Save to CSV
            self.instruments_df.to_csv(self.instruments_file, index=False)
            logger.info(f"✓ Instruments saved to {self.instruments_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error downloading instruments: {str(e)}")
            return False
    
    def load_instruments(self):
        """Load instruments from local CSV"""
        try:
            if self.instruments_file.exists():
                logger.info(f"Loading instruments from {self.instruments_file}")
                self.instruments_df = pd.read_csv(self.instruments_file)
                logger.info(f"✓ Loaded {len(self.instruments_df)} instruments")
                return True
            else:
                logger.warning("Instrument file not found. Downloading...")
                return self.download_instruments()
        except Exception as e:
            logger.error(f"Error loading instruments: {str(e)}")
            return False
    
    def filter_options(self, underlying='NIFTY'):
        """Filter options for specific underlying"""
        if self.instruments_df is None:
            self.load_instruments()
        
        filtered = self.instruments_df[
            (self.instruments_df['underlying'] == underlying) &
            (self.instruments_df['instrument_type'] == 'OPTIDX')
        ]
        
        logger.info(f"Filtered {len(filtered)} {underlying} options")
        return filtered
    
    def get_nearest_expiry(self):
        """Get nearest valid weekly expiry"""
        try:
            if self.instruments_df is None:
                self.load_instruments()
            
            # Get unique expiries and convert to datetime
            expiries = pd.to_datetime(self.instruments_df['expiry'].unique())
            today = datetime.now().date()
            
            # Filter future expiries
            future_expiries = expiries[expiries.date >= today]
            
            if len(future_expiries) == 0:
                logger.error("No valid future expiries found")
                return None
            
            # Sort and get nearest
            nearest = future_expiries.min()
            logger.info(f"Nearest expiry: {nearest.strftime('%Y-%m-%d')}")
            return nearest.strftime('%Y-%m-%d')
            
        except Exception as e:
            logger.error(f"Error getting nearest expiry: {str(e)}")
            return None
    
    def get_atm_strike(self, index_ltp):
        """Calculate ATM strike based on index LTP"""
        strike_interval = config.STRIKE_INTERVAL
        atm_strike = round(index_ltp / strike_interval) * strike_interval
        logger.info(f"Index LTP: {index_ltp}, ATM Strike: {atm_strike}")
        return atm_strike
    
    def get_option_security_id(self, expiry, strike, option_type='CE'):
        """Get security ID for specific option"""
        if self.instruments_df is None:
            self.load_instruments()
        
        try:
            option = self.instruments_df[
                (self.instruments_df['expiry'] == expiry) &
                (self.instruments_df['strike'] == strike) &
                (self.instruments_df['option_type'] == option_type) &
                (self.instruments_df['underlying'] == config.INDEX_NAME)
            ]
            
            if len(option) > 0:
                security_id = option.iloc[0]['security_id']
                logger.info(f"Found {option_type} {strike} (Expiry: {expiry}) - Security ID: {security_id}")
                return security_id
            else:
                logger.warning(f"No option found for {option_type} {strike} expiring {expiry}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting security ID: {str(e)}")
            return None
    
    def _create_sample_instruments(self):
        """Create sample instrument data for testing"""
        # Generate sample data for NIFTY options
        data = []
        
        # Get next 4 weekly expiries (Thursdays)
        today = datetime.now()
        expiries = []
        for i in range(8):
            future_date = today + timedelta(days=i)
            if future_date.weekday() == 3:  # Thursday
                expiries.append(future_date.strftime('%Y-%m-%d'))
            if len(expiries) == 4:
                break
        
        # If no Thursday found, add next week
        if len(expiries) == 0:
            days_until_thursday = (3 - today.weekday()) % 7
            if days_until_thursday == 0:
                days_until_thursday = 7
            next_thursday = today + timedelta(days=days_until_thursday)
            expiries.append(next_thursday.strftime('%Y-%m-%d'))
        
        # Generate strikes around current NIFTY level (assume 23000-24000 range)
        strikes = list(range(22500, 24500, 50))
        
        security_id = 100000
        for expiry in expiries:
            for strike in strikes:
                # CE option
                data.append({
                    'security_id': security_id,
                    'trading_symbol': f'NIFTY {expiry} {strike} CE',
                    'underlying': 'NIFTY',
                    'expiry': expiry,
                    'strike': strike,
                    'option_type': 'CE',
                    'instrument_type': 'OPTIDX',
                    'exchange': 'NSE'
                })
                security_id += 1
                
                # PE option
                data.append({
                    'security_id': security_id,
                    'trading_symbol': f'NIFTY {expiry} {strike} PE',
                    'underlying': 'NIFTY',
                    'expiry': expiry,
                    'strike': strike,
                    'option_type': 'PE',
                    'instrument_type': 'OPTIDX',
                    'exchange': 'NSE'
                })
                security_id += 1
        
        return data