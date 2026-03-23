from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime

from app.models import Base


class AlertConfig(Base):
    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    metric = Column(String(50), nullable=False)
    threshold = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False)

    is_active = Column(Boolean, default=True)


class AlertHistory(Base):
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)

    config_id = Column(Integer, ForeignKey("alert_configs.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    triggered_at = Column(DateTime, default=datetime.utcnow)

    metric_value = Column(Float, nullable=False)
    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False)