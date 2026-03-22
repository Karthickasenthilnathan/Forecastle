from app.models import Product
from sqlalchemy.orm import Session
from datetime import timedelta, date
from fastapi import HTTPException
import random


def generate_mock_forecast(product_id: int, db: Session):
    """
    Generate mock forecast data for a product.
    Used for initial development before ML integration.
    """

    # Validate product exists
    product = db.query(Product).filter(Product.id == product_id).first()
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


def generate_forecast(product_id: int, horizon_days: int, db: Session):
    """
    Generate forecast (placeholder for ML pipeline).
    Later this will call Prophet + XGBoost pipeline.
    """

    # Validate product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    today = date.today()
    forecast = []

    for i in range(horizon_days):
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
        "horizon_days": horizon_days,
        "forecast": forecast,
        "explanation": "Forecast generated using mock model"
    }