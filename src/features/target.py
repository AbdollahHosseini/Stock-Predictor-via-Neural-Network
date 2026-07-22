
import pandas as pd
from stocknn.config import getConfig, getPath


def build_target(df):
    df = df.copy()
    df["target"] = ((df["Close"] - df["Open"]).shift(-1))
    df = df.dropna(subset=["target"])
    df["target"] = (df["target"] >= 0).astype(int)
    return df


def main():
    data = pd.read_csv(getPath("processed", getConfig()['yfinance']['ticker']))
    data = build_target(data)

    output_file = getPath("target", "{ticker}".format(ticker=getConfig()['yfinance']['ticker']))
    data.to_csv(output_file, index=False)

    print(f"Data with target written to {output_file}")


if __name__ == "__main__":
    main()