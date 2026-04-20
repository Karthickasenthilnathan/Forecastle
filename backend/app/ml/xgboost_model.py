import xgboost as xgb
import pandas as pd


def train_xgb(X: pd.DataFrame, y: pd.Series):
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1
    )

    model.fit(X, y)

    return model


def predict_xgb(model, X: pd.DataFrame):
    return model.predict(X)