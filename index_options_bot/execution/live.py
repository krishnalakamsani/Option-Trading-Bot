import logging
from datetime import datetime, timezone
from config.settings import config

logger = logging.getLogger(__name__)

class LiveTrading:
    """Live trading engine using Dhan API"""
    
    def __init__(self, dhan_client):
        self.dhan_client = dhan_client
        self.enabled = (config.TRADING_MODE == 'live')
        
        if not self.enabled:
            logger.warning("⚠️ Live trading is DISABLED. Set TRADING_MODE=live in .env to enable")
    
    def place_order(self, security_id, symbol, price, quantity, transaction_type='BUY'):
        """Place a live order through Dhan API"""
        if not self.enabled:
            logger.error("Live trading is disabled. Cannot place order.")
            return {
                'status': 'failure',
                'error': 'Live trading is disabled'
            }
        
        try:
            logger.info(f"🔴 LIVE ORDER: {transaction_type} {symbol} @ ₹{price} x {quantity}")
            
            response = self.dhan_client.place_order(
                security_id=security_id,
                exchange_segment='NSE_FNO',  # NFO segment
                transaction_type=transaction_type,
                quantity=quantity,
                order_type='MARKET',
                product_type='INTRADAY',
                price=0  # Market order
            )
            
            if response and response.get('status') == 'success':
                order_id = response.get('data', {}).get('orderId')
                logger.info(f"✓ Live order placed successfully. Order ID: {order_id}")
                return response
            else:
                error_msg = response.get('remarks', 'Unknown error') if response else 'No response'
                logger.error(f"Live order failed: {error_msg}")
                return response
                
        except Exception as e:
            logger.error(f"Error placing live order: {str(e)}")
            return {
                'status': 'failure',
                'error': str(e)
            }
    
    def get_order_status(self, order_id):
        """Get status of a live order"""
        if not self.enabled:
            return None
        
        try:
            return self.dhan_client.get_order_status(order_id)
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            return None
    
    def enable_live_trading(self):
        """Enable live trading"""
        self.enabled = True
        logger.warning("⚠️ LIVE TRADING ENABLED")
    
    def disable_live_trading(self):
        """Disable live trading (kill-switch)"""
        self.enabled = False
        logger.critical("🛑 LIVE TRADING DISABLED (Kill-switch activated)")