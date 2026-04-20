from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.forecast_service import generate_forecast
from app.models.forecast import Forecast
from app.db.session import get_db

router = APIRouter(prefix="/forecasts", tags=["Forecasts"])


@router.post("/generate")
async def generate(
    product_id: int,
    horizon_weeks: int = 4,
    session: AsyncSession = Depends(get_db),
):
    """Generate a new forecast for a product using the ML pipeline."""
    result = await generate_forecast(product_id, horizon_weeks, session)

    return {
        "product_id": product_id,
        "horizon_weeks": horizon_weeks,
        "predictions": result["predictions"],
        "confidence": result.get("confidence"),
        "signal_contributions": result["signal_contributions"],
        "explanation": result.get("explanation", "Forecast adjusted using external signals"),
    }


@router.get("/{product_id}")
async def get_latest_forecast(
    product_id: int,
    horizon: int = Query(4, description="Horizon in weeks: 2, 4, or 8"),
    session: AsyncSession = Depends(get_db),
):
    """Get the latest forecast for a product at a given horizon."""
    result = await session.execute(
        select(Forecast)
        .where(
            Forecast.product_id == product_id,
            Forecast.horizon_weeks == horizon,
        )
        .order_by(Forecast.generated_at.desc())
        .limit(1)
    )
    forecast = result.scalar_one_or_none()

    if not forecast:
        return {"error": f"No forecast found for product {product_id} at {horizon}W horizon"}

    return {
        "product_id": product_id,
        "horizon_weeks": forecast.horizon_weeks,
        "forecast_date": str(forecast.forecast_date),
        "predicted_qty": forecast.predicted_qty,
        "lower_bound": forecast.lower_bound,
        "upper_bound": forecast.upper_bound,
        "confidence": forecast.confidence,
        "explanation": forecast.explanation,
        "signal_contributions": forecast.signal_contributions,
        "generated_at": forecast.generated_at.isoformat() if forecast.generated_at else None,
        "is_override": forecast.is_override,
        "override_qty": forecast.override_qty,
    }


@router.get("/{product_id}/history")
async def get_forecast_history(
    product_id: int,
    limit: int = Query(20, le=100),
    session: AsyncSession = Depends(get_db),
):
    """Get forecast version history for a product."""
    result = await session.execute(
        select(Forecast)
        .where(Forecast.product_id == product_id)
        .order_by(Forecast.generated_at.desc())
        .limit(limit)
    )
    forecasts = result.scalars().all()

    return [
        {
            "id": f.id,
            "forecast_date": str(f.forecast_date),
            "generated_at": f.generated_at.isoformat() if f.generated_at else None,
            "horizon_weeks": f.horizon_weeks,
            "predicted_qty": f.predicted_qty,
            "lower_bound": f.lower_bound,
            "upper_bound": f.upper_bound,
            "confidence": f.confidence,
            "explanation": f.explanation,
            "is_override": f.is_override,
            "override_qty": f.override_qty,
        }
        for f in forecasts
    ]


@router.post("/{forecast_id}/override")
async def override_forecast(
    forecast_id: int,
    override_qty: float = Query(..., description="Manual override quantity"),
    session: AsyncSession = Depends(get_db),
):
    """Manually override a forecast's predicted quantity."""
    result = await session.execute(
        select(Forecast).where(Forecast.id == forecast_id)
    )
    forecast = result.scalar_one_or_none()

    if not forecast:
        return {"error": f"Forecast {forecast_id} not found"}

    original_qty = forecast.predicted_qty
    forecast.is_override = True
    forecast.override_qty = override_qty

    await session.commit()

    return {
        "forecast_id": forecast_id,
        "original_qty": original_qty,
        "override_qty": override_qty,
        "impact_pct": round(((override_qty - original_qty) / original_qty) * 100, 2) if original_qty else 0,
        "message": "Forecast override saved successfully",
    }