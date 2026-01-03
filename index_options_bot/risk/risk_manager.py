import logging
import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from config.settings import config

logger = logging.getLogger(__name__)

class RiskManager:
    """Manage risk parameters and trade limits"""
    
    def __init__(self):
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.active_positions = {}
        self.stop_trading = False
        
        # Load today's trades if any
        self._load_today_trades()
    
    def _load_today_trades(self):
        """Load today's trades to calculate current metrics"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            trades_file = config.TRADES_DIR / f'trades_{today}.json'
            
            if trades_file.exists():
                with open(trades_file, 'r') as f:
                    trades = json.load(f)
                    self.daily_trades = len(trades)
                    
                    # Calculate PnL
                    for trade in trades:
                        if 'pnl' in trade:
                            self.daily_pnl += trade['pnl']
                    
                    logger.info(f"Loaded {self.daily_trades} trades, PnL: ₹{self.daily_pnl:.2f}")
        except Exception as e:
            logger.error(f"Error loading today's trades: {str(e)}")
    
    def can_place_trade(self):
        """Check if new trade can be placed based on risk limits"""
        if self.stop_trading:
            logger.warning("⚠️ Trading stopped due to kill-switch")
            return False, "Kill-switch activated"
        
        # Check max trades per day
        if self.daily_trades >= config.MAX_TRADES_PER_DAY:
            logger.warning(f"⚠️ Max trades per day reached: {self.daily_trades}/{config.MAX_TRADES_PER_DAY}")
            return False, "Max trades per day limit reached"
        
        # Check max loss per day
        if self.daily_pnl <= -config.MAX_LOSS_PER_DAY:
            logger.warning(f"⚠️ Max loss per day reached: ₹{self.daily_pnl:.2f}")
            self.stop_trading = True
            return False, "Max loss per day limit reached"
        
        return True, "OK"
    
    def add_position(self, position_id, entry_price, quantity, option_type):
        """Add a new position to track"""
        self.active_positions[position_id] = {
            'entry_price': entry_price,
            'current_price': entry_price,
            'quantity': quantity,
            'option_type': option_type,
            'entry_time': datetime.now(timezone.utc).isoformat(),
            'stop_loss': entry_price * (1 - config.STOP_LOSS_PERCENT / 100),
            'highest_price': entry_price,
            'trailing_stop': None
        }
        logger.info(f"Position added: {position_id} @ ₹{entry_price}")
    
    def update_position(self, position_id, current_price):
        """Update position with current price and check stops"""
        if position_id not in self.active_positions:
            return None
        
        position = self.active_positions[position_id]
        position['current_price'] = current_price
        
        # Update highest price for trailing stop
        if current_price > position['highest_price']:
            position['highest_price'] = current_price
            
            # Update trailing stop
            position['trailing_stop'] = current_price * (1 - config.TRAILING_STOP_PERCENT / 100)
            logger.debug(f"Trailing stop updated: ₹{position['trailing_stop']:.2f}")
        
        # Check stop loss
        if current_price <= position['stop_loss']:
            logger.warning(f"⚠️ Stop Loss hit for {position_id}: ₹{current_price} <= ₹{position['stop_loss']}")
            return 'STOP_LOSS'
        
        # Check trailing stop
        if position['trailing_stop'] and current_price <= position['trailing_stop']:
            logger.warning(f"⚠️ Trailing Stop hit for {position_id}: ₹{current_price} <= ₹{position['trailing_stop']}")
            return 'TRAILING_STOP'
        
        return None
    
    def close_position(self, position_id, exit_price):
        """Close a position and calculate PnL"""
        if position_id not in self.active_positions:
            logger.error(f"Position {position_id} not found")
            return None
        
        position = self.active_positions[position_id]
        
        # Calculate PnL
        pnl = (exit_price - position['entry_price']) * position['quantity']
        pnl_percent = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        
        # Update metrics
        self.daily_pnl += pnl
        self.daily_trades += 1
        
        result = {
            'position_id': position_id,
            'entry_price': position['entry_price'],
            'exit_price': exit_price,
            'quantity': position['quantity'],
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'entry_time': position['entry_time'],
            'exit_time': datetime.now(timezone.utc).isoformat()
        }
        
        # Remove from active positions
        del self.active_positions[position_id]
        
        logger.info(f"✓ Position closed: {position_id}, PnL: ₹{pnl:.2f} ({pnl_percent:.2f}%)")
        return result
    
    def get_active_positions(self):
        """Get all active positions"""
        return self.active_positions
    
    def activate_kill_switch(self):
        """Activate kill-switch to stop all trading"""
        self.stop_trading = True
        logger.critical("🛑 KILL-SWITCH ACTIVATED - All trading stopped")
    
    def deactivate_kill_switch(self):
        """Deactivate kill-switch"""
        self.stop_trading = False
        logger.info("✓ Kill-switch deactivated")
    
    def get_daily_summary(self):
        """Get daily trading summary"""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_trades': self.daily_trades,
            'daily_pnl': self.daily_pnl,
            'active_positions': len(self.active_positions),
            'max_trades_limit': config.MAX_TRADES_PER_DAY,
            'max_loss_limit': config.MAX_LOSS_PER_DAY,
            'kill_switch_active': self.stop_trading
        }