import pandas as pd
from prophet import Prophet


def train_prophet_model(df: pd.DataFrame):
    """
    df must have:
    ds → date
    y → quantity
    """

    model = Prophet()
    model.fit(df)

    return model


def make_forecast(model, periods: int = 28):
    future = model.make_future_dataframe(periods=periods)

    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]