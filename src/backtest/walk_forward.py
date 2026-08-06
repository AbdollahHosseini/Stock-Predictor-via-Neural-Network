import pandas as pd
import numpy as np
from models.train import data_split, get_features_and_target
from stocknn.config import getConfig
from models.xgboost_model import xgboost_pred, accuracy


def walk_forward_xg(train, test, fold_size):
    """
    Perform walk-forward validation on the given training data.

    Args:
        train (pd.DataFrame): The training dataset.
        test (pd.DataFrame): The testing dataset.
        fold_size (int): The size of each fold for walk-forward validation.
    """

    train_chunks = np.array_split(train, len(train) // fold_size)
    test_chunks = np.array_split(test, len(test) // fold_size)

    scores = [0 for _ in range(len(train_chunks) - 1)]

    for i in range(len(train_chunks) - 1):
        X_train = train_chunks[i]
        y_train = test_chunks[i]

        X_test = train_chunks[i + 1]
        y_test = test_chunks[i + 1]

        pred, _ = xgboost_pred(X_train, X_test, y_train)

        acc = accuracy(pred, y_test)
        scores[i] = acc

    return scores




def main():
    ticker = getConfig()['yfinance']['ticker']

    train_df, _, gap_df = data_split("technicals", ticker)
    X_train, y_train = get_features_and_target(train_df)
    X_gap, y_gap = get_features_and_target(gap_df)

    train = pd.concat([X_train, X_gap])
    test = pd.concat([y_train, y_gap])

    scores = walk_forward_xg(train, test, fold_size=len(gap_df))

    print(np.mean(scores), np.std(scores))



if __name__ == "__main__":
    main()
    