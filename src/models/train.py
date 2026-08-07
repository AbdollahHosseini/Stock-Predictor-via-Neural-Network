import pandas as pd
from stocknn.config import getPath, getConfig
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def data_split(fileName, symbol):
    df = pd.read_csv(getPath(fileName, symbol))

    len_df = len(df)
    len_train = int(len_df * 0.7) 
    len_gap = int(len_df * 0.0125)

    train_df = df.iloc[:len_train]
    gap_df = df.iloc[len_train:len_train + len_gap]
    test_df = df.iloc[len_train + len_gap:]

    return train_df, test_df, gap_df

def get_features_and_target(df: pd.DataFrame):
    X = df.drop(columns=['target', 'Date', 'Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume'])
    y = df['target']

    # scaler = MinMaxScaler()

    # X = pd.DataFrame(
    #     scaler.fit_transform(X), 
    #     columns=X.columns
    # )
    
    return X, y


def get_train_test_data(ticker=getConfig()['yfinance']['ticker']):
    train_df, test_df, _ = data_split("technicals", ticker)
    X_train, y_train = get_features_and_target(train_df)
    X_test, y_test = get_features_and_target(test_df)
    return X_train, y_train, X_test, y_test


def main():
    ticker = getConfig()['yfinance']['ticker']
    train_df, test_df, gap_df = data_split("technicals", ticker)
    X_train, y_train, X_test, y_test = get_train_test_data(ticker)
    print(X_train.head(), y_train.head())

if __name__ == "__main__":
    main()