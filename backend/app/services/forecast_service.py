from app.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, date
from fastapi import HTTPException
import random


async def generate_mock_forecast(product_id: int, db: AsyncSession):
    """
    Generate mock forecast data for a product.
    Used for initial development before ML integration.
    """

    # Validate product exists (ASYNC WAY)
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    today = date.today()
    forecast = []

    for i in range(7):
        predicted = random.randint(80, 150)
        lower = predicted - random.randint(10, 30)
        upper = predicted + random.randint(10, 30)

        forecast.append({
            "date": str(today + timedelta(days=i)),
            "predicted_qty": predicted,
            "lower_bound": lower,
            "upper_bound": upper
        })

    return {
        "product_id": product_id,
        "horizon_days": 7,
        "forecast": forecast,
        "explanation": "Forecast generated from mock data"
    }