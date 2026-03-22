from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session 
from fastapi import HTTPException

from app.schemas.product import ProductResponse
from typing import List


from app.models.product import Product
from app.db.session import get_db


router=APIRouter()

@router.get('/products',response_model=List[ProductResponse])
def get_products(db:Session=Depends(get_db)):
    products=db.query(Product).all()
    return products

@router.get("/products/{product_id}",response_model=ProductResponse)
def get_products(product_id:int,db:Session=Depends(get_db)):
    product= db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product