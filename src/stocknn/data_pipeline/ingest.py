from pathlib import Path
import pandas
import yfinance as yf
import yaml
from stocknn.config import getConfig
# from .clean import clean_data

def TickerData():
    config = getConfig()['yfinance']
    ticker = config['ticker']
    start_date = config['start']
    end_date = config['end']
    interval = config['interval']

    data = yf.download(ticker, start=start_date, end=end_date, interval=interval) 

    # data = clean_data(data)

    return data


def write_data_to_csv(data, filename):
    data.to_csv(filename)

def main():
    data = TickerData()
    output_file = Path(__file__).parents[3] / "data" / "raw" / "ticker_data.csv"
    write_data_to_csv(data, output_file)
    print(f"Data written to {output_file}")

