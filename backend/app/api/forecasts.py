from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.forecast import ForecastRequest
from app.services.forecast_service import generate_mock_forecast


router = APIRouter(prefix="/forecasts", tags=["Forecasts"])


@router.get("/{product_id}")
async def get_forecast(product_id: int, db: AsyncSession = Depends(get_db)):
    return await generate_mock_forecast(product_id, db)


@router.post("/")
async def generate_forecast_api(
    request: ForecastRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate forecast based on request payload
    """
    return await generate_mock_forecast(request.product_id, db)