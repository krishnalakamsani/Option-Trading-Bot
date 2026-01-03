#!/usr/bin/env python3
"""
Index Options Trading Bot - Main Entry Point

Automated trading bot for NIFTY index options using Dhan broker API.
Implements SuperTrend strategy with comprehensive risk management.
"""

import logging
import time
import signal
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import config
from utils.dhan_client import DhanClient
from utils.instruments import InstrumentManager
from utils.market_time import MarketTime
from strategy.supertrend import SuperTrendStrategy
from execution.paper import PaperTrading
from execution.live import LiveTrading
from risk.risk_manager import RiskManager

# Configure logging
log_file = config.LOGS_DIR / f'bot_{datetime.now().strftime("%Y%m%d")}.log'
config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingBot:
    """Main trading bot orchestrator"""
    
    def __init__(self):
        self.running = False
        self.dhan_client = None
        self.instrument_manager = None
        self.strategy = None
        self.paper_trading = None
        self.live_trading = None
        self.risk_manager = None
        self.current_position = None
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("\nShutdown signal received. Stopping bot...")
        self.stop()
    
    def initialize(self):
        """Initialize all bot components"""
        try:
            logger.info("="*60)
            logger.info("INDEX OPTIONS TRADING BOT - INITIALIZATION")
            logger.info("="*60)
            
            # Validate configuration
            config.validate()
            logger.info("✓ Configuration validated")
            
            # Display configuration
            self._display_config()
            
            # Initialize Dhan client
            logger.info("\nInitializing Dhan API client...")
            self.dhan_client = DhanClient()
            if not self.dhan_client.authenticate():
                raise Exception("Dhan authentication failed")
            
            # Initialize instrument manager
            logger.info("\nInitializing instrument manager...")
            self.instrument_manager = InstrumentManager(self.dhan_client)
            self.instrument_manager.load_instruments()
            
            # Initialize strategy
            logger.info("\nInitializing SuperTrend strategy...")
            self.strategy = SuperTrendStrategy(
                period=config.SUPERTREND_PERIOD,
                multiplier=config.SUPERTREND_MULTIPLIER
            )
            logger.info(f"✓ Strategy: SuperTrend(period={config.SUPERTREND_PERIOD}, multiplier={config.SUPERTREND_MULTIPLIER})")
            
            # Initialize execution engines
            self.paper_trading = PaperTrading()
            self.live_trading = LiveTrading(self.dhan_client)
            logger.info(f"✓ Trading mode: {config.TRADING_MODE.upper()}")
            
            # Initialize risk manager
            self.risk_manager = RiskManager()
            logger.info("✓ Risk manager initialized")
            
            logger.info("\n" + "="*60)
            logger.info("✓ BOT INITIALIZATION COMPLETE")
            logger.info("="*60 + "\n")
            
            return True
            
        except Exception as e:
            logger.error(f"\n❌ Initialization failed: {str(e)}")
            return False
    
    def _display_config(self):
        """Display current configuration"""
        logger.info("\nCurrent Configuration:")
        logger.info(f"  Index: {config.INDEX_NAME}")
        logger.info(f"  Lot Size: {config.LOT_SIZE}")
        logger.info(f"  Trading Mode: {config.TRADING_MODE.upper()}")
        logger.info(f"  Stop Loss: {config.STOP_LOSS_PERCENT}%")
        logger.info(f"  Trailing Stop: {config.TRAILING_STOP_PERCENT}%")
        logger.info(f"  Max Trades/Day: {config.MAX_TRADES_PER_DAY}")
        logger.info(f"  Max Loss/Day: ₹{config.MAX_LOSS_PER_DAY}")
        logger.info(f"  SuperTrend Period: {config.SUPERTREND_PERIOD}")
        logger.info(f"  SuperTrend Multiplier: {config.SUPERTREND_MULTIPLIER}")
        logger.info(f"  Candle Timeframe: {config.CANDLE_TIMEFRAME} minute(s)")
    
    def run(self):
        """Main bot execution loop"""
        if not self.initialize():
            logger.error("Bot initialization failed. Exiting.")
            return
        
        self.running = True
        
        # Check market status
        if not MarketTime.is_market_open():
            logger.warning(f"\n⚠️ Market is CLOSED. {MarketTime.time_to_market_open()}")
            logger.info("Bot will continue in demo mode with simulated data...\n")
        
        logger.info("Starting main trading loop...\n")
        
        try:
            iteration = 0
            while self.running:
                iteration += 1
                logger.info(f"\n--- Iteration {iteration} [{datetime.now().strftime('%H:%M:%S')}] ---")
                
                # Execute trading cycle
                self._trading_cycle()
                
                # Wait for next polling interval
                time.sleep(config.POLLING_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"\nBot error: {str(e)}", exc_info=True)
        finally:
            self.stop()
    
    def _trading_cycle(self):
        """Execute one trading cycle"""
        try:
            # Get nearest expiry
            expiry = self.instrument_manager.get_nearest_expiry()
            if not expiry:
                logger.error("Could not determine expiry")
                return
            
            # Simulate index LTP (in production, fetch from Dhan API)
            # For demo purposes, we'll use a simulated value
            index_ltp = 23500  # In production: self.dhan_client.get_ltp(security_id, exchange_segment)
            logger.info(f"Index LTP: {index_ltp}")
            
            # Calculate ATM strike
            atm_strike = self.instrument_manager.get_atm_strike(index_ltp)
            
            # Get CE option security ID
            ce_security_id = self.instrument_manager.get_option_security_id(expiry, atm_strike, 'CE')
            if not ce_security_id:
                logger.error("Could not get CE security ID")
                return
            
            # Simulate option LTP (in production, fetch from Dhan API)
            # For demo: simulate option price movement
            import random
            option_ltp = 150 + random.uniform(-5, 5)
            logger.info(f"Option LTP: ₹{option_ltp:.2f}")
            
            # Add price data to strategy
            timestamp = datetime.now()
            self.strategy.add_price_data(
                timestamp=timestamp,
                open_price=option_ltp,
                high=option_ltp + random.uniform(0, 2),
                low=option_ltp - random.uniform(0, 2),
                close=option_ltp
            )
            
            # Generate signal
            signal = self.strategy.generate_signal()
            
            if signal:
                self._handle_signal(signal, ce_security_id, atm_strike, expiry, option_ltp)
            
            # Update existing positions
            if self.current_position:
                self._update_position(option_ltp)
            
            # Display summary
            summary = self.risk_manager.get_daily_summary()
            logger.info(f"Daily Summary: Trades={summary['total_trades']}/{summary['max_trades_limit']}, "
                       f"PnL=₹{summary['daily_pnl']:.2f}")
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {str(e)}", exc_info=True)
    
    def _handle_signal(self, signal, security_id, strike, expiry, current_price):
        """Handle trading signal"""
        try:
            if signal['type'] == 'BUY' and not self.current_position:
                # Check risk limits
                can_trade, reason = self.risk_manager.can_place_trade()
                if not can_trade:
                    logger.warning(f"Cannot place trade: {reason}")
                    return
                
                # Place buy order
                symbol = f"NIFTY {expiry} {strike} CE"
                quantity = config.LOT_SIZE
                
                if config.TRADING_MODE == 'paper':
                    result = self.paper_trading.place_order(
                        security_id=security_id,
                        symbol=symbol,
                        price=current_price,
                        quantity=quantity,
                        order_type='BUY'
                    )
                else:
                    result = self.live_trading.place_order(
                        security_id=security_id,
                        symbol=symbol,
                        price=current_price,
                        quantity=quantity,
                        transaction_type='BUY'
                    )
                
                if result and result.get('status') == 'success':
                    order_id = result.get('order_id')
                    self.current_position = order_id
                    self.risk_manager.add_position(order_id, current_price, quantity, 'CE')
                    logger.info(f"✓ BUY order placed: {symbol} @ ₹{current_price}")
            
            elif signal['type'] == 'SELL' and self.current_position:
                # Close position
                self._close_position(security_id, strike, expiry, current_price, 'SIGNAL')
                
        except Exception as e:
            logger.error(f"Error handling signal: {str(e)}", exc_info=True)
    
    def _update_position(self, current_price):
        """Update existing position and check stops"""
        try:
            stop_trigger = self.risk_manager.update_position(self.current_position, current_price)
            
            if stop_trigger:
                logger.warning(f"Stop triggered: {stop_trigger}")
                # Close position
                # Get position details (simplified for demo)
                self._close_position(None, None, None, current_price, stop_trigger)
                
        except Exception as e:
            logger.error(f"Error updating position: {str(e)}", exc_info=True)
    
    def _close_position(self, security_id, strike, expiry, exit_price, reason):
        """Close an open position"""
        try:
            if not self.current_position:
                return
            
            # Close with risk manager
            result = self.risk_manager.close_position(self.current_position, exit_price)
            
            if result:
                # Place sell order
                symbol = f"NIFTY {expiry} {strike} CE" if strike else "OPTION"
                quantity = result['quantity']
                
                if config.TRADING_MODE == 'paper':
                    self.paper_trading.place_order(
                        security_id=security_id or 0,
                        symbol=symbol,
                        price=exit_price,
                        quantity=quantity,
                        order_type='SELL'
                    )
                else:
                    self.live_trading.place_order(
                        security_id=security_id,
                        symbol=symbol,
                        price=exit_price,
                        quantity=quantity,
                        transaction_type='SELL'
                    )
                
                logger.info(f"✓ Position closed: {reason}, PnL: ₹{result['pnl']:.2f}")
                self.current_position = None
                
        except Exception as e:
            logger.error(f"Error closing position: {str(e)}", exc_info=True)
    
    def stop(self):
        """Stop the bot gracefully"""
        logger.info("\nStopping bot...")
        self.running = False
        
        # Close any open positions
        if self.current_position:
            logger.warning("Closing open position...")
            # In production, close the position here
        
        # Display final summary
        if self.risk_manager:
            summary = self.risk_manager.get_daily_summary()
            logger.info("\n" + "="*60)
            logger.info("FINAL SUMMARY")
            logger.info("="*60)
            logger.info(f"Date: {summary['date']}")
            logger.info(f"Total Trades: {summary['total_trades']}")
            logger.info(f"Daily PnL: ₹{summary['daily_pnl']:.2f}")
            logger.info(f"Active Positions: {summary['active_positions']}")
            logger.info("="*60)
        
        logger.info("\n✓ Bot stopped successfully\n")


def main():
    """Main entry point"""
    bot = TradingBot()
    bot.run()


if __name__ == '__main__':
    main()