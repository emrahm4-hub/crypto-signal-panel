# Crypto Signal Panel

**Kripto para sinyal paneli - Order flow analizi ve real-time trading signals**

Advanced cryptocurrency trading signal panel featuring the VPMVT V2 (Volume-Price-Momentum-Volatility-Time) composite indicator for comprehensive market analysis.

## Features

- **VPMVT V2 Indicator**: Advanced composite indicator combining 5 market dimensions
- **Real-time Analysis**: Order flow and volume analysis
- **Customizable Parameters**: Adjust weights and periods for each component
- **Signal Generation**: Automated buy/sell signal detection
- **Multi-timeframe Support**: Works with any timeframe data
- **Extensible Framework**: Easy to add new indicators

## VPMVT V2 Indicator

The VPMVT V2 is a sophisticated technical indicator that combines five key market dimensions:

### Components

1. **Volume (V)** - 20%
   - Money Flow Index (MFI)
   - Volume Rate of Change (VROC)
   - On-Balance Volume (OBV) momentum
   - Measures buying and selling pressure

2. **Price (P)** - 20%
   - Price position vs Moving Averages (SMA, EMA)
   - Price Rate of Change
   - Trend strength (ADX-style calculation)
   - Identifies price trends and momentum

3. **Momentum (M)** - 20%
   - Relative Strength Index (RSI)
   - Stochastic Oscillator
   - Momentum Rate of Change
   - Captures market momentum and overbought/oversold conditions

4. **Volatility (V)** - 20%
   - Average True Range (ATR)
   - Standard Deviation
   - Bollinger Band Width
   - Measures market volatility and risk

5. **Time (T)** - 20%
   - Volume-Weighted Average Price (VWAP)
   - Time-Weighted Momentum
   - Exponential Moving Average distance
   - Incorporates time-decay factors

### Output

The VPMVT V2 produces a composite score from **0 to 100**:

- **80-100**: Very Strong (bullish)
- **60-79**: Strong (bullish)
- **40-59**: Moderate (neutral)
- **20-39**: Weak (bearish)
- **0-19**: Very Weak (bearish)

### Signal Generation

- **Buy Signal**: VPMVT V2 crosses above 70 (default)
- **Sell Signal**: VPMVT V2 crosses below 30 (default)
- Thresholds are fully customizable

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/emrahm4-hub/crypto-signal-panel.git
cd crypto-signal-panel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from backend.indicators.vpmvt_v2 import VPMVT_V2
import pandas as pd

# Load your OHLCV data
df = pd.DataFrame({
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...]
})

# Initialize the indicator
vpmvt = VPMVT_V2()

# Calculate the indicator
df['VPMVT_V2'] = vpmvt.calculate(df)

# Generate trading signals
df['signal'] = vpmvt.get_signal(df, buy_threshold=70, sell_threshold=30)

# Get signal strength
df['strength'] = vpmvt.get_strength(df)

print(df[['close', 'VPMVT_V2', 'signal', 'strength']].tail())
```

### Custom Component Weights

```python
# Emphasize momentum and volume
vpmvt = VPMVT_V2(
    volume_weight=0.30,      # 30%
    price_weight=0.15,       # 15%
    momentum_weight=0.35,    # 35%
    volatility_weight=0.10,  # 10%
    time_weight=0.10         # 10%
)

df['VPMVT_V2'] = vpmvt.calculate(df)
```

### Analyze Individual Components

```python
# Get all component scores separately
components = vpmvt.calculate_components(df)

print("Volume Score:", components['volume'].iloc[-1])
print("Price Score:", components['price'].iloc[-1])
print("Momentum Score:", components['momentum'].iloc[-1])
print("Volatility Score:", components['volatility'].iloc[-1])
print("Time Score:", components['time'].iloc[-1])
print("Composite Score:", components['composite'].iloc[-1])
```

### Run Examples

```bash
python examples/vpmvt_v2_example.py
```

This will run 5 comprehensive examples demonstrating:
1. Basic usage
2. Custom component weights
3. Individual component analysis
4. Signal generation
5. Simple backtest simulation

## Project Structure

```
crypto-signal-panel/
├── backend/
│   ├── indicators/          # Technical indicators
│   │   ├── base_indicator.py   # Base class for all indicators
│   │   └── vpmvt_v2.py         # VPMVT V2 implementation
│   ├── data/                # Data fetching and processing
│   ├── signals/             # Signal generation logic
│   ├── api/                 # REST API endpoints
│   └── utils/               # Utility functions
├── examples/
│   └── vpmvt_v2_example.py  # Usage examples
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── config/                  # Configuration files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

### Indicator Parameters

All parameters can be customized when initializing the indicator:

```python
vpmvt = VPMVT_V2(
    # Period settings
    volume_period=20,       # Volume calculation period
    price_period=20,        # Price calculation period
    momentum_period=14,     # Momentum calculation period
    volatility_period=14,   # Volatility calculation period
    time_period=20,         # Time calculation period

    # Component weights (will be normalized to sum to 1.0)
    volume_weight=0.20,
    price_weight=0.20,
    momentum_weight=0.20,
    volatility_weight=0.20,
    time_weight=0.20
)
```

### Signal Thresholds

Customize buy/sell signal thresholds:

```python
# Conservative (fewer signals, higher quality)
signals = vpmvt.get_signal(df, buy_threshold=75, sell_threshold=25)

# Aggressive (more signals, lower quality)
signals = vpmvt.get_signal(df, buy_threshold=65, sell_threshold=35)
```

## API Reference

### VPMVT_V2 Class

#### Constructor
```python
VPMVT_V2(
    volume_period=20,
    price_period=20,
    momentum_period=14,
    volatility_period=14,
    time_period=20,
    volume_weight=0.20,
    price_weight=0.20,
    momentum_weight=0.20,
    volatility_weight=0.20,
    time_weight=0.20
)
```

#### Methods

- `calculate(df)` - Calculate composite VPMVT V2 score (0-100)
- `calculate_components(df)` - Get all individual component scores
- `get_signal(df, buy_threshold=70, sell_threshold=30)` - Generate trading signals
- `get_strength(df)` - Get signal strength classification
- `add_to_dataframe(df, column_name=None)` - Add indicator to DataFrame

## Use Cases

### 1. Trend Following
Use high VPMVT V2 values (>70) to identify strong uptrends and enter long positions.

### 2. Mean Reversion
Use extreme VPMVT V2 values (<20 or >80) for potential reversal trades.

### 3. Divergence Detection
Compare VPMVT V2 trends with price trends to spot divergences.

### 4. Multi-Timeframe Analysis
Apply VPMVT V2 on multiple timeframes for confirmation.

### 5. Risk Management
Use the volatility component to adjust position sizing.

## Advanced Features

### Component Weighting Strategies

#### Momentum-Focused (Day Trading)
```python
vpmvt = VPMVT_V2(
    momentum_weight=0.40,
    volume_weight=0.30,
    price_weight=0.15,
    volatility_weight=0.10,
    time_weight=0.05
)
```

#### Volatility-Focused (Risk Management)
```python
vpmvt = VPMVT_V2(
    volatility_weight=0.35,
    volume_weight=0.25,
    momentum_weight=0.20,
    price_weight=0.15,
    time_weight=0.05
)
```

#### Balanced (All Markets)
```python
vpmvt = VPMVT_V2(
    volume_weight=0.20,
    price_weight=0.20,
    momentum_weight=0.20,
    volatility_weight=0.20,
    time_weight=0.20
)
```

## Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=backend tests/
```

## Performance Considerations

- The indicator calculates multiple rolling windows and statistical measures
- Minimum recommended data: 100+ periods for accurate calculations
- Uses vectorized pandas/numpy operations for efficiency
- Suitable for real-time streaming with incremental updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational and research purposes only. Trading cryptocurrencies carries risk. Always do your own research and never invest more than you can afford to lose.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [ ] WebSocket integration for real-time data
- [ ] REST API endpoints
- [ ] Web dashboard with interactive charts
- [ ] Additional technical indicators
- [ ] Machine learning signal optimization
- [ ] Multi-exchange support
- [ ] Backtesting framework
- [ ] Alert system (Telegram, Discord, Email)

## Acknowledgments

- Inspired by traditional technical analysis indicators
- Built for the cryptocurrency trading community
- Special thanks to the open-source trading community

---

**Kripto Para Sinyal Paneli** - Profesyonel seviye teknik analiz ve sinyal üretimi sistemi.
