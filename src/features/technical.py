import pandas as pd

def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index. Bounded 0-100 by definition — verify this holds."""
    ...

def compute_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Returns (macd_line, signal_line, histogram)."""
    ...

def compute_lag_features(series: pd.Series, lags: list[int]) -> pd.DataFrame:
    """Returns a DataFrame of lagged columns, one per value in `lags`."""
    ...

def add_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Orchestrator: calls each compute_* function, assembles result columns onto df."""
    ...