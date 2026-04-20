from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.product import ProductCreate, ProductResponse
from app.models.product import Product
from app.models.forecast import Forecast
from app.db.session import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    """List all products."""
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single product with its latest forecast summary."""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    # Get latest forecast
    forecast_result = await db.execute(
        select(Forecast)
        .where(Forecast.product_id == product_id)
        .order_by(Forecast.generated_at.desc())
        .limit(1)
    )
    latest_forecast = forecast_result.scalar_one_or_none()

    response = {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "category": product.category,
        "unit": product.unit,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }

    if latest_forecast:
        response["latest_forecast"] = {
            "forecast_date": str(latest_forecast.forecast_date),
            "predicted_qty": latest_forecast.predicted_qty,
            "confidence": latest_forecast.confidence,
            "generated_at": latest_forecast.generated_at.isoformat() if latest_forecast.generated_at else None,
        }
    else:
        response["latest_forecast"] = None

    return response


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new product."""
    new_product = Product(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product