import logging
import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from config.settings import config

logger = logging.getLogger(__name__)

class PaperTrading:
    """Paper trading engine for simulation"""
    
    def __init__(self):
        self.positions = {}
        self.trades = []
        self.capital = 100000  # Starting virtual capital
        
        # Ensure directories exist
        config.TRADES_DIR.mkdir(parents=True, exist_ok=True)
        config.PNL_DIR.mkdir(parents=True, exist_ok=True)
    
    def place_order(self, security_id, symbol, price, quantity, order_type='BUY'):
        """Simulate order placement"""
        try:
            order_id = f"PAPER_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{security_id}"
            
            trade = {
                'order_id': order_id,
                'security_id': security_id,
                'symbol': symbol,
                'order_type': order_type,
                'price': price,
                'quantity': quantity,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'status': 'COMPLETED'
            }
            
            if order_type == 'BUY':
                # Add to positions
                self.positions[order_id] = {
                    'security_id': security_id,
                    'symbol': symbol,
                    'entry_price': price,
                    'quantity': quantity,
                    'entry_time': trade['timestamp']
                }
                logger.info(f"💰 PAPER BUY: {symbol} @ ₹{price} x {quantity}")
            else:
                # SELL - remove from positions
                if order_id in self.positions:
                    del self.positions[order_id]
                logger.info(f"💸 PAPER SELL: {symbol} @ ₹{price} x {quantity}")
            
            self.trades.append(trade)
            self._save_trade(trade)
            
            return {
                'status': 'success',
                'order_id': order_id,
                'data': trade
            }
            
        except Exception as e:
            logger.error(f"Error in paper trading: {str(e)}")
            return {
                'status': 'failure',
                'error': str(e)
            }
    
    def get_positions(self):
        """Get all active positions"""
        return self.positions
    
    def get_trades(self):
        """Get all trades"""
        return self.trades
    
    def _save_trade(self, trade):
        """Save trade to file"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Save as JSON
            json_file = config.TRADES_DIR / f'trades_{today}.json'
            trades_list = []
            
            if json_file.exists():
                with open(json_file, 'r') as f:
                    trades_list = json.load(f)
            
            trades_list.append(trade)
            
            with open(json_file, 'w') as f:
                json.dump(trades_list, f, indent=2)
            
            # Save as CSV
            csv_file = config.TRADES_DIR / f'trades_{today}.csv'
            file_exists = csv_file.exists()
            
            with open(csv_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=trade.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(trade)
            
        except Exception as e:
            logger.error(f"Error saving trade: {str(e)}")
    
    def calculate_pnl(self):
        """Calculate total PnL"""
        total_pnl = 0
        
        for trade in self.trades:
            if trade['order_type'] == 'SELL' and 'pnl' in trade:
                total_pnl += trade['pnl']
        
        return total_pnl