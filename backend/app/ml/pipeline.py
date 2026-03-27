import pandas as pd
from sqlalchemy import select

from app.models.sales import Sales
from app.db.session import AsyncSessionLocal
from app.ml.prophet_model import train_prophet_model, make_forecast


from app.ml.feature_engine import generate_signal_features


async def generate_forecast(product_id: int, horizon_weeks: int = 4):
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Sales).where(Sales.product_id == product_id)
        )

        sales = result.scalars().all()

        if not sales:
            return {"error": "No sales data found"}

        # Convert to dataframe
        df = pd.DataFrame([
            {
                "ds": s.date,
                "y": s.quantity
            }
            for s in sales
        ])

        # Train model
        model = train_prophet_model(df)

        # Forecast (weeks → days)
        periods = horizon_weeks * 7

        forecast = make_forecast(model, periods)

        # Take only future predictions
        future = forecast.tail(periods)

        features = generate_signal_features(product_id)

        adjustment_factor = (
            1
            + 0.1 * features["sentiment_score"]
            + 0.05 * features["weather_index"]
            - 0.05 * features["supply_risk"]
)

        future["yhat"] = future["yhat"] * adjustment_factor
        future["yhat_lower"] = future["yhat_lower"] * adjustment_factor
        future["yhat_upper"] = future["yhat_upper"] * adjustment_factor

        return {
    "predictions": future.to_dict(orient="records"),
    "features": features
}