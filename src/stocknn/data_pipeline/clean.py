from stocknn.data_pipeline.ingest import TickerData, write_data_to_csv
from pathlib import Path
import polars as pl

def clean_data(data):
    """
    Cleans the input data by removing rows with missing values.

    Parameters:
    data (pl.DataFrame): The input data to be cleaned.

    Returns:
    pl.DataFrame: The cleaned data with rows containing missing values removed.
    """
    return data.drop_nulls()


def main():
    data = TickerData()
    data = clean_data(data)
    output_file = Path(__file__).parents[3] / "data" / "processed" / "ticker_data.csv"
    write_data_to_csv(data, output_file)
    print(f"Data written to {output_file}")


if __name__ == "__main__":
    main()