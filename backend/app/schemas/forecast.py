from pydantic import BaseModel
from typing import List,Dict,Optional
from datetime import datetime
class ForecastRequest(BaseModel):
    product_id:int
    horizon_days:int=7

class ForecastPoint(BaseModel):
    
