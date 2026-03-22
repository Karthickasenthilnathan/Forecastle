from pydantic import BaseModel

class ForecastRequest(BaseModel):
    product_id:int
    horizon_days:int=7