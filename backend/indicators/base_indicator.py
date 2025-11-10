"""
Base Indicator Class
Abstract base class for all technical indicators
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any


class BaseIndicator(ABC):
    """
    Abstract base class for all technical indicators

    All indicators should inherit from this class and implement the calculate method
    """

    def __init__(self, name: str, short_name: str):
        """
        Initialize the indicator

        Args:
            name: Full name of the indicator
            short_name: Short name/abbreviation for the indicator
        """
        self.name = name
        self.short_name = short_name
        self.values = None
        self.params = {}

    @abstractmethod
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.Series:
        """
        Calculate indicator values

        Args:
            df: DataFrame with OHLCV data (open, high, low, close, volume)
            **kwargs: Additional parameters for the indicator

        Returns:
            pd.Series: Calculated indicator values with same index as input df
        """
        pass

    def add_to_dataframe(self, df: pd.DataFrame, column_name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Add calculated indicator to dataframe

        Args:
            df: DataFrame with OHLCV data
            column_name: Custom column name (uses short_name if not provided)
            **kwargs: Additional parameters for the indicator

        Returns:
            pd.DataFrame: Input dataframe with added indicator column
        """
        col_name = column_name if column_name else self.short_name
        df[col_name] = self.calculate(df, **kwargs)
        self.values = df[col_name]
        return df

    def get_signal(self, df: pd.DataFrame, **kwargs) -> pd.Series:
        """
        Generate trading signals based on indicator

        Args:
            df: DataFrame with OHLCV data and calculated indicator
            **kwargs: Additional parameters for signal generation

        Returns:
            pd.Series: Trading signals (1=buy, -1=sell, 0=neutral)
        """
        return pd.Series(0, index=df.index)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', short_name='{self.short_name}')"
