#!/usr/bin/env python3
"""
Quick test script to validate bot components
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import config
from utils.market_time import MarketTime
from strategy.supertrend import SuperTrendStrategy
import random
from datetime import datetime

def test_config():
    print("\n" + "="*60)
    print("Testing Configuration...")
    print("="*60)
    try:
        config.validate()
        print("✓ Configuration valid")
        print(f"  - Trading Mode: {config.TRADING_MODE}")
        print(f"  - Index: {config.INDEX_NAME}")
        print(f"  - Lot Size: {config.LOT_SIZE}")
        print(f"  - Stop Loss: {config.STOP_LOSS_PERCENT}%")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_market_time():
    print("\n" + "="*60)
    print("Testing Market Time...")
    print("="*60)
    try:
        is_open = MarketTime.is_market_open()
        current_time = MarketTime.get_current_time()
        print(f"✓ Current Time (IST): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  - Market Open: {is_open}")
        if not is_open:
            print(f"  - {MarketTime.time_to_market_open()}")
        return True
    except Exception as e:
        print(f"✗ Market time error: {e}")
        return False

def test_supertrend():
    print("\n" + "="*60)
    print("Testing SuperTrend Strategy...")
    print("="*60)
    try:
        strategy = SuperTrendStrategy(period=7, multiplier=4)
        print(f"✓ Strategy initialized (Period={strategy.period}, Multiplier={strategy.multiplier})")
        
        # Simulate price data
        print("\n  Simulating price data...")
        base_price = 150
        for i in range(20):
            price = base_price + random.uniform(-10, 10)
            high = price + random.uniform(1, 3)
            low = price - random.uniform(1, 3)
            strategy.add_price_data(
                timestamp=datetime.now(),
                open_price=price,
                high=high,
                low=low,
                close=price
            )
        
        print(f"  - Added {len(strategy.price_data)} candles")
        
        # Calculate SuperTrend
        st_data = strategy.calculate_supertrend()
        if st_data:
            print(f"\n  ✓ SuperTrend calculated successfully")
            print(f"    - Close: ₹{st_data['close']:.2f}")
            print(f"    - SuperTrend: ₹{st_data['supertrend']:.2f}")
            print(f"    - Direction: {'UPTREND' if st_data['direction'] == 1 else 'DOWNTREND'}")
        else:
            print("  ✗ SuperTrend calculation failed")
            return False
        
        # Generate signal
        signal = strategy.generate_signal()
        if signal:
            print(f"\n  🎯 Signal Generated: {signal['type']} at ₹{signal['price']:.2f}")
        else:
            print("  - No signal (no trend change)")
        
        return True
    except Exception as e:
        print(f"✗ SuperTrend error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("INDEX OPTIONS TRADING BOT - COMPONENT TEST")
    print("="*60)
    
    results = []
    results.append(("Configuration", test_config()))
    results.append(("Market Time", test_market_time()))
    results.append(("SuperTrend Strategy", test_supertrend()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! Bot is ready to run.")
        print("\nRun the bot with: python main.py")
    else:
        print("\n✗ Some tests failed. Please fix the issues before running the bot.")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    exit(main())