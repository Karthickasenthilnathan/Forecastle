from pydantic import BaseModel

class ProductResponse(BaseModel):
    id:int
    name:str
    sku:str

    class Config:
        from_attributes=True
