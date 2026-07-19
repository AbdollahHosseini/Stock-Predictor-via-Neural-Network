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

        if data.empty:
            raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}")
        elif data.head(1).index[0] > (pd.to_datetime(start_date) + pd.Timedelta(days=3)): 
            # At most 3 days of data are missing at the start of the requested date range. Weekend + 1 extra day for holidays. If more than 3 days are missing, raise an error.
            raise ValueError(f"Data for {ticker} starts after the requested start date {start_date}")
        elif data.tail(1).index[0] < (pd.to_datetime(end_date) - pd.Timedelta(days=3)):
            raise ValueError(f"Data for {ticker} ends before the requested end date {end_date}")
        else:
            data.columns = data.columns.get_level_values(0)
            return pl.DataFrame(data.reset_index())

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pl.DataFrame()


def write_data_to_csv(data, filename):
    data.write_csv(filename)

def main():
    data = TickerData()

    if data.is_empty():
        print("No data to write to CSV.")
        return
    else:
        output_file = Path(__file__).parents[3] / "data" / "raw" / "{ticker}_data.csv".format(ticker=getConfig()['yfinance']['ticker'])
        write_data_to_csv(data, output_file)
        print(f"Data written to {output_file}")


if __name__ == "__main__":
    main()

