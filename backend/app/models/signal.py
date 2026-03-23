from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.models import Base


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    date = Column(Date, nullable=False)

    source = Column(String(50), nullable=False)
    signal_name = Column(String(100), nullable=False)

    signal_value = Column(Float, nullable=False)

    raw_payload = Column(JSONB, nullable=True)

    collected_at = Column(DateTime, default=datetime.utcnow)