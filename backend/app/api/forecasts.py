from fastapi import APIRouter


from app.ml.pipeline import generate_forecast


router = APIRouter(prefix="/forecasts", tags=["Forecasts"])


@router.post("/generate")
async def generate(product_id: int, horizon_weeks: int = 4):
    result = await generate_forecast(product_id, horizon_weeks)

    return {
        "product_id": product_id,
        "horizon_weeks": horizon_weeks,
        "predictions": result["predictions"],
        "signal_contribution": result["features"],
        "explanation": "Forecast adjusted using external signals"
    }
@router.get("/{product_id}/history")
async def forecast_history(product_id: int):
    return {"product_id": product_id, "history": []}
@router.post("/{forecast_id}/override")
async def override_forecast(forecast_id: int):
    return {"message": f"Override for forecast {forecast_id}"}