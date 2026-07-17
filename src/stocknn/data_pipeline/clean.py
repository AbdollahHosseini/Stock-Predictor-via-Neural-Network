from stocknn.data_pipeline.ingest import write_data_to_csv
from stocknn.config import getConfig
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


def test_data(data):
    assert not data.is_empty(), "DataFrame is empty after cleaning."
    assert data.null_count().sum_horizontal().item() == 0, "DataFrame still contains null values after cleaning."
    assert data.shape[0] > 0, "DataFrame has no rows after cleaning."
    assert data.is_sorted("Date"), "Date column is sorted in ascending order."
    assert data.is_unique().all() == True, "Date column contains duplicate values."

def main():
    data = pl.read_csv(Path(__file__).parents[3] / "data" / "raw" / "{ticker}_data.csv".format(ticker=getConfig()['yfinance']['ticker']))
    data = clean_data(data)
    output_file = Path(__file__).parents[3] / "data" / "processed" / "{ticker}_data.csv".format(ticker=getConfig()['yfinance']['ticker'])
    write_data_to_csv(data, output_file)
    print(f"Data written to {output_file}")
    test_data(data)


if __name__ == "__main__":
    main()