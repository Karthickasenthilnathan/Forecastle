from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session 
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.schemas.product import ProductCreate, ProductResponse


from typing import List


from app.models.product import Product
from app.db.session import get_db


router=APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    new_product = Product(**product.dict())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product