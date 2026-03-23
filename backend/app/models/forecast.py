from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.models import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    forecast_date = Column(Date, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    horizon_weeks = Column(Integer, nullable=False)

    predicted_qty = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=False)
    upper_bound = Column(Float, nullable=False)

    confidence = Column(Float, nullable=True)

    model_version = Column(String(50), nullable=True)

    explanation = Column(Text, nullable=True)

    signal_contributions = Column(JSONB, nullable=True)

    is_override = Column(Boolean, default=False)
    override_qty = Column(Float, nullable=True)