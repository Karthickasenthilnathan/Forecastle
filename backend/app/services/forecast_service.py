from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.ml.pipeline import run_pipeline   # ✅ MISSING IMPORT
from app.services.explanation_service import generate_explanation
from app.models.forecast import Forecast


async def generate_forecast(
    product_id: int,
    horizon: int,
    session: AsyncSession
):
    # 1. Run ML pipeline
    result = await run_pipeline(product_id, horizon)

    # ✅ SAFETY: avoid KeyError crashes
    predictions = result.get("predictions", [])
    features = result.get("features", {})
    confidence = result.get("confidence", 0.8)

    # 2. Generate explanation
    explanation = generate_explanation(features)

    saved_forecasts = []

    # 3. Save each prediction
    for pred in predictions:
        forecast = Forecast(
            product_id=product_id,

            # ✅ safer key access (prevents crashes if keys differ)
            forecast_date=pred.get("date"),
            horizon_weeks=horizon,
            predicted_qty=pred.get("yhat"),
            lower_bound=pred.get("yhat_lower"),
            upper_bound=pred.get("yhat_upper"),

            confidence=confidence,
            model_version="v1",
            explanation=explanation,
            signal_contributions=features,
            generated_at=datetime.utcnow()
        )

        session.add(forecast)
        saved_forecasts.append(forecast)

    # ✅ commit once after loop (good practice)
    await session.commit()

    # 4. Return response
    return {
        "predictions": predictions,
        "explanation": explanation,
        "signal_contributions": features,
        "confidence": confidence
    }