import pandas as pd
from stocknn.config import getConfig, getPath

def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index. Bounded 0-100 by definition — verify this holds."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0).abs()

    sample = pd.DataFrame({"gain": gain, "loss": loss})

    sample["avg_gain"] = sample["gain"].rolling(window=window).mean()
    sample["avg_loss"] = sample["loss"].rolling(window=window).mean().add(1e-10)  # Avoid division by zero
    sample["rs"] = sample["avg_gain"] / sample["avg_loss"]
    sample["rsi"] = 100 - (100 / (1 + sample["rs"]))

    return sample['rsi']

def compute_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Returns (macd_line, signal_line, histogram)."""
    MACD_line = close.ewm(span=fast, adjust=False).mean() - close.ewm(span=slow, adjust=False).mean()
    signal_line = MACD_line.ewm(span=signal, adjust=False).mean()
    histogram = MACD_line - signal_line
    return MACD_line, signal_line, histogram

def compute_lag_features(series: pd.Series, lags: list[int]) -> pd.DataFrame:
    """Returns a DataFrame of lagged columns, one per value in `lags`."""
    ...

def add_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Orchestrator: calls each compute_* function, assembles result columns onto df."""
    ...

def main():
    try:
        data = pd.read_csv(getPath("target", getConfig()['yfinance']['ticker']))

        data['rsi'] = compute_rsi(data["Close"])
        data['macd_line'], data['signal_line'], data['histogram'] = compute_macd(data["Close"])
        print(data.head(30))
        # data_with_features = data # Change to add_all_features(data)

        # output_file = getPath("technical", "{ticker}_data_with_features.csv".format(ticker=getConfig()['yfinance']['ticker']))
        # data_with_features.to_csv(output_file, index=False)
        # print(f"Data with features written to {output_file}")
        # print(getConfig()['yfinance']['ticker'])

    except Exception as e:
        print(f"Error in main: {e}")

main()