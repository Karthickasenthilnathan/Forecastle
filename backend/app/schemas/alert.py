from pydantic import BaseModel
from datetime import datetime


class AlertConfigCreate(BaseModel):
    product_id: int
    metric: str
    threshold: float
    direction: str


class AlertResponse(BaseModel):
    id: int
    product_id: int
    metric: str
    threshold: float
    direction: str
    is_active: bool

    class Config:
        from_attributes = True


class AlertHistoryResponse(BaseModel):
    id: int
    product_id: int
    message: str
    metric_value: float
    triggered_at: datetime
    is_read: bool

    class Config:
        from_attributes = True