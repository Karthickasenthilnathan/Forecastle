from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forecast import Forecast
from app.services.explanation_service import generate_explanation


async def generate_forecast(product_id: int, horizon: int, session: AsyncSession):
    from app.ml.pipeline import run_pipeline

    result = await run_pipeline(product_id, horizon)

    predictions = result.get("predictions", [])
    features = result.get("features", {})
    confidence = result.get("confidence", 0.8)
    explanation = generate_explanation(features)
    generated_at = datetime.utcnow()

    saved_forecasts = []

    for pred in predictions:
        predicted_qty = pred.get("yhat", pred.get("predicted_qty", pred.get("qty")))
        lower_bound = pred.get("yhat_lower", pred.get("lower_bound", pred.get("lower")))
        upper_bound = pred.get("yhat_upper", pred.get("upper_bound", pred.get("upper")))

        forecast = Forecast(
            product_id=product_id,
            forecast_date=pred.get("date"),
            horizon_weeks=horizon,
            predicted_qty=predicted_qty,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            confidence=confidence,
            model_version="v1",
            explanation=explanation,
            signal_contributions=features,
            generated_at=generated_at,
        )

        session.add(forecast)
        saved_forecasts.append(forecast)

    await session.commit()

    return {
        "predictions": predictions,
        "explanation": explanation,
        "signal_contributions": features,
        "confidence": confidence,
        "forecast_id": saved_forecasts[0].id if saved_forecasts else None,
    }
