from matplotlib import pyplot
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from models.train import get_train_test_data
from xgboost import plot_importance


def xgboost_pred(train_X, test_X, train_Y, params={'objective':'binary:logistic', 'max_depth':3, 'learning_rate':0.05, 'n_estimators':100,'alpha':10}):
    """
    Train and evaluate an XGBoost model.

    Args:
        train (pd.DataFrame): Training dataset.
        test (pd.DataFrame): Testing dataset.
        target (str): Target variable name.
        params (dict, optional): Hyperparameters for the XGBoost model. Defaults to None.

    Returns: 
        model: Trained XGBoost model.
        accuracy (float): Accuracy of the model on the test set.
    """

    model = XGBClassifier(**params)
    model.fit(train_X, train_Y)

    y_pred = model.predict(test_X)

    return y_pred, model.feature_importances_, model


def accuracy(prediction, Y_test):
    return accuracy_score(prediction, Y_test)


def main():
    X_train, y_train, X_test, y_test = get_train_test_data()
    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    pred, importances, _ = xgboost_pred(X_train, X_test, y_train)
    print("XGBoost Model Accuracy is:", accuracy(pred, y_test))

    for i, importance in enumerate(importances):
        print(f"{importance}: {X_train.columns[i]}")

if __name__ == "__main__":
    main()
    