"""
VPMVT V2 Indicator
Volume-Price-Momentum-Volatility-Time Composite Indicator

This advanced indicator combines multiple market dimensions to provide
comprehensive trading signals for cryptocurrency markets.

Components:
- Volume (V): Volume trend analysis
- Price (P): Price action and trend
- Momentum (M): Rate of change and momentum oscillators
- Volatility (V): Market volatility measurement
- Time (T): Time-weighted factors
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from .base_indicator import BaseIndicator


class VPMVT_V2(BaseIndicator):
    """
    VPMVT V2 - Advanced Composite Technical Indicator

    Combines five key market dimensions:
    1. Volume - Volume trend and money flow
    2. Price - Price action and moving averages
    3. Momentum - RSI, ROC, and momentum indicators
    4. Volatility - ATR and standard deviation
    5. Time - Time-weighted price and volume

    Each component is normalized to a 0-100 scale and combined with configurable weights.
    """

    def __init__(
        self,
        volume_period: int = 20,
        price_period: int = 20,
        momentum_period: int = 14,
        volatility_period: int = 14,
        time_period: int = 20,
        volume_weight: float = 0.20,
        price_weight: float = 0.20,
        momentum_weight: float = 0.20,
        volatility_weight: float = 0.20,
        time_weight: float = 0.20
    ):
        """
        Initialize VPMVT V2 Indicator

        Args:
            volume_period: Period for volume calculations
            price_period: Period for price calculations
            momentum_period: Period for momentum calculations
            volatility_period: Period for volatility calculations
            time_period: Period for time-weighted calculations
            volume_weight: Weight for volume component (0-1)
            price_weight: Weight for price component (0-1)
            momentum_weight: Weight for momentum component (0-1)
            volatility_weight: Weight for volatility component (0-1)
            time_weight: Weight for time component (0-1)
        """
        super().__init__("VPMVT V2", "VPMVT_V2")

        self.volume_period = volume_period
        self.price_period = price_period
        self.momentum_period = momentum_period
        self.volatility_period = volatility_period
        self.time_period = time_period

        # Normalize weights to sum to 1
        total_weight = volume_weight + price_weight + momentum_weight + volatility_weight + time_weight
        self.volume_weight = volume_weight / total_weight
        self.price_weight = price_weight / total_weight
        self.momentum_weight = momentum_weight / total_weight
        self.volatility_weight = volatility_weight / total_weight
        self.time_weight = time_weight / total_weight

        self.params = {
            'volume_period': volume_period,
            'price_period': price_period,
            'momentum_period': momentum_period,
            'volatility_period': volatility_period,
            'time_period': time_period,
            'volume_weight': self.volume_weight,
            'price_weight': self.price_weight,
            'momentum_weight': self.momentum_weight,
            'volatility_weight': self.volatility_weight,
            'time_weight': self.time_weight
        }

    def _calculate_volume_component(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Volume Component (0-100 scale)

        Combines:
        - Volume Rate of Change (VROC)
        - Money Flow Index (MFI)
        - On-Balance Volume (OBV) momentum

        Returns:
            pd.Series: Normalized volume score (0-100)
        """
        # Money Flow Index (MFI)
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        raw_money_flow = typical_price * df['volume']

        # Positive and negative money flow
        positive_flow = raw_money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = raw_money_flow.where(typical_price < typical_price.shift(1), 0)

        positive_mf = positive_flow.rolling(window=self.volume_period).sum()
        negative_mf = negative_flow.rolling(window=self.volume_period).sum()

        mfi = 100 - (100 / (1 + (positive_mf / (negative_mf + 1e-10))))

        # Volume Rate of Change
        vroc = (df['volume'] / df['volume'].shift(self.volume_period) - 1) * 100
        vroc_normalized = 50 + (vroc / vroc.rolling(100).std()).clip(-2, 2) * 25

        # On-Balance Volume momentum
        obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        obv_roc = obv.pct_change(self.volume_period) * 100
        obv_normalized = 50 + (obv_roc / obv_roc.rolling(100).std()).clip(-2, 2) * 25

        # Combine components
        volume_score = (mfi * 0.4 + vroc_normalized * 0.3 + obv_normalized * 0.3).clip(0, 100)

        return volume_score.fillna(50)

    def _calculate_price_component(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Price Component (0-100 scale)

        Combines:
        - Price position relative to moving averages
        - Price Rate of Change
        - Trend strength

        Returns:
            pd.Series: Normalized price score (0-100)
        """
        # Moving averages
        sma = df['close'].rolling(window=self.price_period).mean()
        ema = df['close'].ewm(span=self.price_period, adjust=False).mean()

        # Price position (0-100)
        price_vs_sma = ((df['close'] - sma) / sma * 100).clip(-50, 50) + 50
        price_vs_ema = ((df['close'] - ema) / ema * 100).clip(-50, 50) + 50

        # Price Rate of Change
        roc = (df['close'] / df['close'].shift(self.price_period) - 1) * 100
        roc_normalized = 50 + (roc / roc.rolling(100).std()).clip(-2, 2) * 25

        # Trend strength using ADX-like calculation
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=self.price_period).mean()

        up_move = df['high'] - df['high'].shift()
        down_move = df['low'].shift() - df['low']
        plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0)
        minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0)

        plus_di = 100 * (plus_dm.rolling(self.price_period).mean() / (atr + 1e-10))
        minus_di = 100 * (minus_dm.rolling(self.price_period).mean() / (atr + 1e-10))

        trend_strength = np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10) * 100
        trend_direction = np.where(plus_di > minus_di, 1, -1)
        trend_score = 50 + (trend_strength * trend_direction * 0.5)

        # Combine components
        price_score = (
            price_vs_sma * 0.3 +
            price_vs_ema * 0.3 +
            roc_normalized * 0.2 +
            trend_score * 0.2
        ).clip(0, 100)

        return price_score.fillna(50)

    def _calculate_momentum_component(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Momentum Component (0-100 scale)

        Combines:
        - RSI (Relative Strength Index)
        - Stochastic Oscillator
        - Rate of Change

        Returns:
            pd.Series: Normalized momentum score (0-100)
        """
        # RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=self.momentum_period).mean()
        avg_loss = loss.rolling(window=self.momentum_period).mean()

        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))

        # Stochastic Oscillator
        lowest_low = df['low'].rolling(window=self.momentum_period).min()
        highest_high = df['high'].rolling(window=self.momentum_period).max()

        stoch_k = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low + 1e-10))
        stoch_d = stoch_k.rolling(window=3).mean()

        # Momentum (Rate of Change)
        momentum = ((df['close'] - df['close'].shift(self.momentum_period)) /
                   df['close'].shift(self.momentum_period) * 100)
        momentum_normalized = 50 + (momentum / momentum.rolling(100).std()).clip(-2, 2) * 25

        # Combine components
        momentum_score = (
            rsi * 0.4 +
            stoch_k * 0.3 +
            momentum_normalized * 0.3
        ).clip(0, 100)

        return momentum_score.fillna(50)

    def _calculate_volatility_component(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Volatility Component (0-100 scale)

        Combines:
        - Average True Range (ATR)
        - Standard Deviation
        - Bollinger Band Width

        Returns:
            pd.Series: Normalized volatility score (0-100)
        """
        # Average True Range (ATR)
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=self.volatility_period).mean()
        atr_pct = (atr / df['close']) * 100

        # Normalize ATR (lower volatility = higher score for stability)
        atr_normalized = 100 - (atr_pct / atr_pct.rolling(100).quantile(0.95) * 100).clip(0, 100)

        # Standard Deviation
        returns = df['close'].pct_change()
        std_dev = returns.rolling(window=self.volatility_period).std() * np.sqrt(252) * 100
        std_normalized = 100 - (std_dev / std_dev.rolling(100).quantile(0.95) * 100).clip(0, 100)

        # Bollinger Band Width
        sma = df['close'].rolling(window=self.volatility_period).mean()
        bb_std = df['close'].rolling(window=self.volatility_period).std()
        upper_band = sma + (bb_std * 2)
        lower_band = sma - (bb_std * 2)
        bb_width = ((upper_band - lower_band) / sma) * 100
        bb_normalized = 100 - (bb_width / bb_width.rolling(100).quantile(0.95) * 100).clip(0, 100)

        # Combine components (inverse relationship: high volatility = low score)
        volatility_score = (
            atr_normalized * 0.4 +
            std_normalized * 0.3 +
            bb_normalized * 0.3
        ).clip(0, 100)

        return volatility_score.fillna(50)

    def _calculate_time_component(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Time Component (0-100 scale)

        Combines:
        - Time-Weighted Average Price (TWAP)
        - Volume-Weighted Average Price (VWAP)
        - Exponential decay factor

        Returns:
            pd.Series: Normalized time score (0-100)
        """
        # Volume-Weighted Average Price (VWAP)
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap = (typical_price * df['volume']).rolling(window=self.time_period).sum() / \
               df['volume'].rolling(window=self.time_period).sum()

        # Price vs VWAP
        price_vs_vwap = ((df['close'] - vwap) / vwap * 100).clip(-50, 50) + 50

        # Time-weighted momentum (recent data weighted more)
        weights = np.exp(np.linspace(-1, 0, self.time_period))
        weights = weights / weights.sum()

        def weighted_momentum(series):
            if len(series) < self.time_period:
                return np.nan
            returns = series.pct_change().fillna(0)
            recent_returns = returns.iloc[-self.time_period:]
            return np.sum(recent_returns.values * weights) * 100

        time_momentum = df['close'].rolling(window=self.time_period).apply(weighted_momentum, raw=False)
        time_momentum_normalized = 50 + (time_momentum / time_momentum.rolling(100).std()).clip(-2, 2) * 25

        # Exponential moving average distance
        ema_short = df['close'].ewm(span=int(self.time_period/2), adjust=False).mean()
        ema_long = df['close'].ewm(span=self.time_period, adjust=False).mean()
        ema_distance = ((ema_short - ema_long) / ema_long * 100).clip(-50, 50) + 50

        # Combine components
        time_score = (
            price_vs_vwap * 0.4 +
            time_momentum_normalized * 0.3 +
            ema_distance * 0.3
        ).clip(0, 100)

        return time_score.fillna(50)

    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.Series:
        """
        Calculate VPMVT V2 composite indicator

        Args:
            df: DataFrame with OHLCV data (open, high, low, close, volume)
            **kwargs: Additional parameters

        Returns:
            pd.Series: VPMVT V2 composite score (0-100)
        """
        # Validate required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Calculate individual components
        volume_score = self._calculate_volume_component(df)
        price_score = self._calculate_price_component(df)
        momentum_score = self._calculate_momentum_component(df)
        volatility_score = self._calculate_volatility_component(df)
        time_score = self._calculate_time_component(df)

        # Calculate weighted composite score
        vpmvt_v2 = (
            volume_score * self.volume_weight +
            price_score * self.price_weight +
            momentum_score * self.momentum_weight +
            volatility_score * self.volatility_weight +
            time_score * self.time_weight
        )

        return vpmvt_v2.clip(0, 100)

    def calculate_components(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate all individual components separately

        Args:
            df: DataFrame with OHLCV data

        Returns:
            Dict containing all component scores
        """
        return {
            'volume': self._calculate_volume_component(df),
            'price': self._calculate_price_component(df),
            'momentum': self._calculate_momentum_component(df),
            'volatility': self._calculate_volatility_component(df),
            'time': self._calculate_time_component(df),
            'composite': self.calculate(df)
        }

    def get_signal(self, df: pd.DataFrame, buy_threshold: float = 70, sell_threshold: float = 30) -> pd.Series:
        """
        Generate trading signals based on VPMVT V2 values

        Args:
            df: DataFrame with OHLCV data
            buy_threshold: VPMVT V2 value above which to generate buy signal (default: 70)
            sell_threshold: VPMVT V2 value below which to generate sell signal (default: 30)

        Returns:
            pd.Series: Trading signals (1=buy, -1=sell, 0=neutral)
        """
        vpmvt = self.calculate(df)
        signals = pd.Series(0, index=df.index)

        # Buy signal: VPMVT crosses above buy_threshold
        signals[(vpmvt > buy_threshold) & (vpmvt.shift(1) <= buy_threshold)] = 1

        # Sell signal: VPMVT crosses below sell_threshold
        signals[(vpmvt < sell_threshold) & (vpmvt.shift(1) >= sell_threshold)] = -1

        return signals

    def get_strength(self, df: pd.DataFrame) -> pd.Series:
        """
        Get signal strength classification

        Args:
            df: DataFrame with OHLCV data

        Returns:
            pd.Series: Signal strength ('Very Strong', 'Strong', 'Moderate', 'Weak', 'Very Weak')
        """
        vpmvt = self.calculate(df)

        conditions = [
            vpmvt >= 80,
            vpmvt >= 60,
            vpmvt >= 40,
            vpmvt >= 20,
            vpmvt < 20
        ]

        choices = ['Very Strong', 'Strong', 'Moderate', 'Weak', 'Very Weak']

        return pd.Series(np.select(conditions, choices), index=df.index)
