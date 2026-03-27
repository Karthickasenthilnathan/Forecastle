from pydantic import BaseModel
from datetime import datetime


class SignalResponse(BaseModel):
    source: str
    signal_name: str
    signal_value: float
    collected_at: datetime