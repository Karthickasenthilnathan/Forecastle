from pydantic import BaseModel
from typing import List,Dict,Optional
from datetime import datetime
from datetime import date
class ForecastRequest(BaseModel):
    product_id:int
    horizon_days:int=7
class ForecastPoint(BaseModel):
    date: date
    predicted_qty: float
    lower_bound: float
    upper_bound: float


class ForecastResponse(BaseModel):
    product_id: int
    horizon_weeks: int

    predictions: List[ForecastPoint]

    confidence: Optional[float]
    explanation: Optional[str]

    signal_contributions: Optional[Dict[str, float]]

    generated_at: datetime
