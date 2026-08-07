from models.train import data_split
import pandas as pd

def get_baseline_predictions():
    """Naive baseline model that predicts the next day's target will be the same as today's target."""
    _, test_df, gap_df = data_split("technicals", "AAPL")
    print(test_df.shape)
    test_df['baseline_prediction'] = test_df['target'].shift(1)
    test_df.iloc[0, test_df.columns.get_loc('baseline_prediction')] = gap_df['target'].iloc[-1]  # Set the first prediction to the last value of the gap_df
    return (test_df['target'] == test_df['baseline_prediction']).sum() / len(test_df)  # Return accuracy of baseline predictions

def main():
    baseline_predictions = get_baseline_predictions()
    print(baseline_predictions)

if __name__ == "__main__":
    main()