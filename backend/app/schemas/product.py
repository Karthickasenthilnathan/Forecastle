from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name:str

    sku:str
    category:Optional[str]=None
    unit:Optional[str]="units"
class ProductCreate(ProductBase):
    pass
class ProductResponse(ProductBase):
    id:int
    created_at:datetime

    class Config:
        from_attributes=True



