import pandas as pd
from pathlib import Path
import yfinance as yf
from stocknn.config import getConfig
import polars as pl

def TickerData():
    config = getConfig()['yfinance']
    ticker = config['ticker']
    start_date = config['start']
    end_date = config['end']
    interval = config['interval']

    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval, auto_adjust=False)

        data.columns = data.columns.get_level_values(0)

        return pl.DataFrame(data.reset_index())

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pl.DataFrame()


def write_data_to_csv(data, filename):
    data.write_csv(filename)

def main():
    data = TickerData()
    output_file = Path(__file__).parents[3] / "data" / "raw" / "{ticker}_data.csv".format(ticker=getConfig()['yfinance']['ticker'])
    write_data_to_csv(data, output_file)
    print(f"Data written to {output_file}")


if __name__ == "__main__":
    main()

