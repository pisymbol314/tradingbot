#!/usr/bin/env python3
"""
Simple SPX RSI Monitor Script
Use this to get started before full bot automation

Run: python rsi_monitor.py
"""

import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import time

def get_spy_data():
    """Get SPY data as proxy for SPX"""
    try:
        spy = yf.Ticker("SPY")
        data = spy.history(period="100d")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_rsi(data, period=14):
    """Calculate RSI indicator"""
    data['rsi'] = ta.rsi(data['Close'], length=period)
    return data

def check_signal(data, rsi_threshold=35):
    """Check if RSI signal is triggered"""
    current_rsi = data['rsi'].iloc[-1]
    current_price = data['Close'].iloc[-1]
    previous_rsi = data['rsi'].iloc[-2]

    # Signal: RSI crosses below threshold
    signal = current_rsi < rsi_threshold and previous_rsi >= rsi_threshold

    return {
        'signal': signal,
        'current_rsi': current_rsi,
        'current_price': current_price,
        'timestamp': datetime.now()
    }

def display_status(result):
    """Display current market status"""
    print("\n" + "="*50)
    print("📊 SPX Bull Put Strategy Monitor")
    print("="*50)
    print(f"⏰ Time: {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💰 SPY Price: ${result['current_price']:.2f}")
    print(f"📈 RSI (14): {result['current_rsi']:.2f}")

    if result['signal']:
        print("\n🚨 SIGNAL DETECTED! 🚨")
        print("Action: Consider Bull Put Spread")
        print("Details:")
        print("  1. Sell SPY puts at-the-money (2 weeks expiry)")
        print("  2. Buy SPY puts $1-2 below")  
        print("  3. Target 50% profit")
        print("  4. Close 1 week before expiration")
    else:
        threshold_diff = result['current_rsi'] - 35
        print(f"\n⏳ No Signal (RSI {threshold_diff:+.1f} above threshold)")
        print("Waiting for RSI < 35...")

def main():
    """Main monitoring loop"""
    print("Starting SPX Bull Put Strategy Monitor...")
    print("Press Ctrl+C to stop")

    try:
        while True:
            # Get market data
            data = get_spy_data()
            if data is None:
                print("Failed to get market data, retrying in 60 seconds...")
                time.sleep(60)
                continue

            # Calculate RSI
            data = calculate_rsi(data)

            # Check for signals
            result = check_signal(data)

            # Display status
            display_status(result)

            # Wait 5 minutes before next check
            print("\nNext check in 5 minutes...")
            time.sleep(300)  # 5 minutes

    except KeyboardInterrupt:
        print("\n\nMonitor stopped by user. Happy trading! 📈")

if __name__ == "__main__":
    main()
