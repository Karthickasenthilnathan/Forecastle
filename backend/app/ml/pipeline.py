import pandas as pd
from sqlalchemy import select

from app.models.sales import Sales
from app.db.session import AsyncSessionLocal
from app.ml.prophet_model import train_prophet_model, make_forecast
from app.ml.feature_engine import generate_signal_features
from app.ml.xgboost_model import train_xgb, predict_xgb


async def generate_forecast(product_id: int, horizon_weeks: int = 4):

    async with AsyncSessionLocal() as db:

        # -------------------------
        # 1. FETCH SALES DATA
        # -------------------------
        result = await db.execute(
            select(Sales).where(Sales.product_id == product_id)
        )

        sales = result.scalars().all()

        if not sales:
            return {"error": "No sales data found"}

        # -------------------------
        # 2. PREPARE DATAFRAME
        # -------------------------
        df = pd.DataFrame([
            {"ds": s.date, "y": s.quantity}
            for s in sales
        ])

        # -------------------------
        # 3. TRAIN PROPHET
        # -------------------------
        model = train_prophet_model(df)

        periods = horizon_weeks * 7
        forecast = make_forecast(model, periods)

        future = forecast.tail(periods).copy()

        # ==================================================
        # 4. XGBOOST TRAINING
        # ==================================================

        feature_rows = []
        targets = []
        base_features = await generate_signal_features(product_id)
        for s in sales:
            feature_rows.append(base_features)
            targets.append(s.quantity)

        X = pd.DataFrame(feature_rows)
        y = pd.Series(targets)

        xgb_model = train_xgb(X, y)

        # ==================================================
        # 5. PREDICT FUTURE ADJUSTMENT
        # ==================================================

        future_features = []

        for _ in range(periods):
            future_features.append(base_features)

        X_future = pd.DataFrame(future_features)

        xgb_adjustment = predict_xgb(xgb_model, X_future)

        # ==================================================
        # 6. COMBINE WITH PROPHET
        # ==================================================

        future["yhat"] = future["yhat"].values + xgb_adjustment
        future["yhat_lower"] = future["yhat_lower"].values + xgb_adjustment
        future["yhat_upper"] = future["yhat_upper"].values + xgb_adjustment

        # -------------------------
        # 7. BUILD RESPONSE
        # -------------------------
        predictions = [
            {
                "date": row["ds"].date() if hasattr(row["ds"], "date") else row["ds"],
                "yhat": round(float(row["yhat"]), 2),
                "yhat_lower": round(float(row["yhat_lower"]), 2),
                "yhat_upper": round(float(row["yhat_upper"]), 2),
            }
            for _, row in future.iterrows()
        ]

        yhat_range = future["yhat_upper"] - future["yhat_lower"]
        mean_range = yhat_range.mean() if len(yhat_range) > 0 else 1.0
        confidence = float(round(max(0.0, min(1.0, 1.0 - (mean_range / (future["yhat"].abs().mean() + 1e-9)))), 2))

        return {
            "predictions": predictions,
            "confidence": confidence,
            "features": base_features,
        }


# Alias used by forecast_service.py
run_pipeline = generate_forecast