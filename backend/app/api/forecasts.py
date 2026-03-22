from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.forecast import ForecastRequest
from app.services.forecast_service import (
    generate_forecast,
    generate_mock_forecast
)

router = APIRouter(prefix="/forecasts", tags=["Forecasts"])


@router.get("/{product_id}")
def get_forecast(product_id: int, db: Session = Depends(get_db)):
    """
    Get mock forecast for a product (GET endpoint)
    Example: /forecasts/1
    """
    return generate_mock_forecast(product_id, db)


@router.post("/")
def generate_forecast_api(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """
    Generate forecast based on request payload
    """
    return generate_forecast(
        request.product_id,
        request.horizon_days,
        db
    )