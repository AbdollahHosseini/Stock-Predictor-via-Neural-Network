from pathlib import Path
import yfinance as yf
import yaml
from stocknn.data_pipeline import getConfig


def TickerData():
    config = getConfig()['yfinance']
    ticker = config['ticker']
    start_date = config['start']
    end_date = config['end']
    interval = config['interval']

    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

    return data.dropna()



def write_data_to_csv(data, filename):
    data.to_csv(filename)

def main():

    data = TickerData()
    output_file = Path(__file__).parents[3] / "data" / "raw" / "ticker_data.csv"
    write_data_to_csv(data, output_file)
    print(f"Data written to {output_file}")



if __name__ == "__main__":
    main()