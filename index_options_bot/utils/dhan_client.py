import logging
from dhanhq import dhanhq
from config.settings import config

logger = logging.getLogger(__name__)

class DhanClient:
    """Wrapper for Dhan API client"""
    
    def __init__(self):
        self.client = None
        self.authenticated = False
        
    def authenticate(self):
        """Authenticate with Dhan API"""
        try:
            logger.info("Authenticating with Dhan API...")
            self.client = dhanhq(config.DHAN_CLIENT_ID, config.DHAN_ACCESS_TOKEN)
            
            # Validate connection by fetching fund limits
            funds = self.client.get_fund_limits()
            
            if funds and 'status' in funds:
                if funds['status'] == 'success':
                    self.authenticated = True
                    logger.info("✓ Authentication successful")
                    logger.info(f"Available Balance: ₹{funds.get('data', {}).get('availabelBalance', 'N/A')}")
                    return True
                else:
                    logger.error(f"Authentication failed: {funds.get('remarks', 'Unknown error')}")
                    return False
            else:
                logger.error("Authentication failed: Invalid response from Dhan API")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            self.authenticated = False
            return False
    
    def get_fund_limits(self):
        """Get fund limits"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        return self.client.get_fund_limits()
    
    def get_ltp(self, security_id, exchange_segment):
        """Get Last Traded Price for a security"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            response = self.client.get_ltp_data(exchange_segment, str(security_id))
            if response and response.get('status') == 'success':
                return response.get('data', {}).get('LTP')
            return None
        except Exception as e:
            logger.error(f"Error fetching LTP for security {security_id}: {str(e)}")
            return None
    
    def get_historical_data(self, security_id, exchange_segment, instrument_type, from_date, to_date):
        """Get historical candle data"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            response = self.client.historical_daily_data(
                security_id=str(security_id),
                exchange_segment=exchange_segment,
                instrument_type=instrument_type,
                from_date=from_date,
                to_date=to_date
            )
            return response
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return None
    
    def place_order(self, security_id, exchange_segment, transaction_type, quantity, 
                   order_type, product_type, price=0):
        """Place an order"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            response = self.client.place_order(
                security_id=str(security_id),
                exchange_segment=exchange_segment,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                product_type=product_type,
                price=price
            )
            return response
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return None
    
    def get_order_status(self, order_id):
        """Get order status"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            response = self.client.get_order_by_id(order_id)
            return response
        except Exception as e:
            logger.error(f"Error fetching order status: {str(e)}")
            return None