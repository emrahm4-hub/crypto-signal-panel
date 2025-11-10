"""
VPMVT V2 Indicator - Example Usage

This script demonstrates how to use the VPMVT V2 indicator
for cryptocurrency trading signal generation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.indicators.vpmvt_v2 import VPMVT_V2


def generate_sample_data(days=100):
    """
    Generate sample OHLCV data for testing

    Args:
        days: Number of days of data to generate

    Returns:
        pd.DataFrame: Sample OHLCV data
    """
    dates = pd.date_range(end=datetime.now(), periods=days, freq='1H')

    # Generate realistic price data with trend and noise
    np.random.seed(42)
    base_price = 50000
    trend = np.linspace(0, 5000, days)
    noise = np.random.randn(days) * 500
    close = base_price + trend + noise.cumsum() * 0.1

    # Generate OHLCV data
    high = close * (1 + np.random.uniform(0, 0.02, days))
    low = close * (1 - np.random.uniform(0, 0.02, days))
    open_price = low + (high - low) * np.random.uniform(0.3, 0.7, days)
    volume = np.random.uniform(100, 1000, days) * (1 + np.random.randn(days) * 0.3)

    df = pd.DataFrame({
        'timestamp': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

    df.set_index('timestamp', inplace=True)
    return df


def example_basic_usage():
    """Example 1: Basic VPMVT V2 calculation"""
    print("=" * 80)
    print("EXAMPLE 1: Basic VPMVT V2 Usage")
    print("=" * 80)

    # Generate sample data
    df = generate_sample_data(days=200)

    # Initialize VPMVT V2 indicator with default parameters
    vpmvt = VPMVT_V2()

    # Calculate indicator
    df['VPMVT_V2'] = vpmvt.calculate(df)

    # Display recent values
    print("\nRecent VPMVT V2 values:")
    print(df[['close', 'volume', 'VPMVT_V2']].tail(10))

    # Get current signal strength
    df['strength'] = vpmvt.get_strength(df)
    print(f"\nCurrent Signal Strength: {df['strength'].iloc[-1]}")
    print(f"Current VPMVT V2 Value: {df['VPMVT_V2'].iloc[-1]:.2f}")


def example_custom_weights():
    """Example 2: VPMVT V2 with custom component weights"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Component Weights")
    print("=" * 80)

    # Generate sample data
    df = generate_sample_data(days=200)

    # Initialize with custom weights (emphasize momentum and volume)
    vpmvt = VPMVT_V2(
        volume_weight=0.30,      # 30% weight on volume
        price_weight=0.15,       # 15% weight on price
        momentum_weight=0.35,    # 35% weight on momentum
        volatility_weight=0.10,  # 10% weight on volatility
        time_weight=0.10         # 10% weight on time
    )

    print("\nIndicator Parameters:")
    for key, value in vpmvt.params.items():
        print(f"  {key}: {value}")

    # Calculate indicator
    df['VPMVT_V2'] = vpmvt.calculate(df)

    print("\nRecent values with custom weights:")
    print(df[['close', 'VPMVT_V2']].tail(5))


def example_component_analysis():
    """Example 3: Analyze individual components"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Individual Component Analysis")
    print("=" * 80)

    # Generate sample data
    df = generate_sample_data(days=200)

    # Initialize indicator
    vpmvt = VPMVT_V2()

    # Calculate all components
    components = vpmvt.calculate_components(df)

    # Add all components to dataframe
    for name, values in components.items():
        df[f'{name}_score'] = values

    # Display recent component values
    print("\nRecent component scores:")
    component_cols = ['volume_score', 'price_score', 'momentum_score',
                     'volatility_score', 'time_score', 'composite_score']
    print(df[component_cols].tail(5).round(2))

    # Component statistics
    print("\nComponent Statistics (last 50 periods):")
    print(df[component_cols].tail(50).describe().round(2))


def example_signal_generation():
    """Example 4: Generate trading signals"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Trading Signal Generation")
    print("=" * 80)

    # Generate sample data
    df = generate_sample_data(days=200)

    # Initialize indicator
    vpmvt = VPMVT_V2()

    # Calculate indicator and signals
    df['VPMVT_V2'] = vpmvt.calculate(df)
    df['signal'] = vpmvt.get_signal(df, buy_threshold=70, sell_threshold=30)
    df['strength'] = vpmvt.get_strength(df)

    # Find all buy and sell signals
    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]

    print(f"\nTotal Buy Signals: {len(buy_signals)}")
    print(f"Total Sell Signals: {len(sell_signals)}")

    if len(buy_signals) > 0:
        print("\nRecent Buy Signals:")
        print(buy_signals[['close', 'VPMVT_V2', 'strength']].tail(3))

    if len(sell_signals) > 0:
        print("\nRecent Sell Signals:")
        print(sell_signals[['close', 'VPMVT_V2', 'strength']].tail(3))

    # Display current status
    current_signal = df['signal'].iloc[-1]
    current_value = df['VPMVT_V2'].iloc[-1]
    current_strength = df['strength'].iloc[-1]

    print(f"\nCurrent Status:")
    print(f"  Signal: {'BUY' if current_signal == 1 else 'SELL' if current_signal == -1 else 'NEUTRAL'}")
    print(f"  VPMVT V2 Value: {current_value:.2f}")
    print(f"  Strength: {current_strength}")


def example_backtest_simulation():
    """Example 5: Simple backtest simulation"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Simple Backtest Simulation")
    print("=" * 80)

    # Generate sample data
    df = generate_sample_data(days=500)

    # Initialize indicator
    vpmvt = VPMVT_V2()

    # Calculate signals
    df['VPMVT_V2'] = vpmvt.calculate(df)
    df['signal'] = vpmvt.get_signal(df, buy_threshold=65, sell_threshold=35)

    # Simple backtest logic
    position = 0
    entry_price = 0
    trades = []

    for i in range(len(df)):
        if df['signal'].iloc[i] == 1 and position == 0:  # Buy signal
            position = 1
            entry_price = df['close'].iloc[i]
            trades.append({
                'type': 'BUY',
                'timestamp': df.index[i],
                'price': entry_price,
                'vpmvt': df['VPMVT_V2'].iloc[i]
            })
        elif df['signal'].iloc[i] == -1 and position == 1:  # Sell signal
            position = 0
            exit_price = df['close'].iloc[i]
            pnl = (exit_price - entry_price) / entry_price * 100
            trades.append({
                'type': 'SELL',
                'timestamp': df.index[i],
                'price': exit_price,
                'vpmvt': df['VPMVT_V2'].iloc[i],
                'pnl': pnl
            })

    # Calculate statistics
    completed_trades = [t for t in trades if t['type'] == 'SELL']

    if completed_trades:
        total_trades = len(completed_trades)
        winning_trades = len([t for t in completed_trades if t['pnl'] > 0])
        total_pnl = sum([t['pnl'] for t in completed_trades])
        avg_pnl = total_pnl / total_trades
        win_rate = (winning_trades / total_trades) * 100

        print(f"\nBacktest Results:")
        print(f"  Total Trades: {total_trades}")
        print(f"  Winning Trades: {winning_trades}")
        print(f"  Win Rate: {win_rate:.2f}%")
        print(f"  Total P&L: {total_pnl:.2f}%")
        print(f"  Average P&L per Trade: {avg_pnl:.2f}%")

        print("\nLast 5 Trades:")
        for trade in completed_trades[-5:]:
            print(f"  {trade['timestamp']} - SELL @ ${trade['price']:.2f} - "
                  f"P&L: {trade['pnl']:.2f}% - VPMVT: {trade['vpmvt']:.2f}")
    else:
        print("\nNo completed trades in the simulation period.")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "VPMVT V2 INDICATOR - EXAMPLES" + " " * 29 + "║")
    print("║" + " " * 10 + "Volume-Price-Momentum-Volatility-Time Composite" + " " * 20 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        example_basic_usage()
        example_custom_weights()
        example_component_analysis()
        example_signal_generation()
        example_backtest_simulation()

        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
