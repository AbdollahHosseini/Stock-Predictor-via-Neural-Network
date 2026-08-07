import pandas as pd
import numpy as np
from models.train import data_split, get_features_and_target
from stocknn.config import getConfig, getPath
from models.xgboost_model import xgboost_pred, accuracy

    
def xg_walk_forward(df, fold_size):
    """
        perform walk-forward validation on the given training data.

    Args:
        df (pd.DataFrame): The training dataset.
        fold_size (int): The size of each fold for walk-forward validation.
    """

    X, y = get_features_and_target(df)

    X_chunks = np.array_split(X, len(X) // fold_size)
    y_chunks = np.array_split(y, len(y) // fold_size)

    scores = [0 for _ in range(len(X_chunks) - 1)]
    X = pd.DataFrame()
    y = pd.DataFrame()

    train_pred = []

    for i in range(len(X_chunks) - 1):

        X = pd.concat([X, X_chunks[i]])
        y = pd.concat([y, y_chunks[i]])

        X_test = X_chunks[i + 1][14:]
        y_test = y_chunks[i + 1][14:]

        pred, _, model = xgboost_pred(X, X_test, y)

        train_pred.append(accuracy(model.predict(X), y))
        scores[i] = accuracy(pred, y_test)

    return scores, train_pred
        

def main():
    ticker = getConfig()['yfinance']['ticker']
    df = pd.read_csv(getPath("technicals", ticker))

    score, train_score = xg_walk_forward(df, int(len(df) * 0.05))

    print(f"Walk-forward validation scores: {score}, 'mean': {np.mean(score)}, 'std': {np.std(score)}")
    print(f"Training scores: {train_score}, 'mean': {np.mean(train_score)}, 'std': {np.std(train_score)}")


if __name__ == "__main__":
    main()
