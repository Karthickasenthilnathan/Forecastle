from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.models import Base


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)

    model_name = Column(String(100), nullable=False)   # 'prophet_base', 'xgboost_signal'
    version = Column(String(50), nullable=False)        # 'v1', 'v2', etc.

    artifact_path = Column(String(500), nullable=False) # Path to serialized model file

    metrics = Column(JSONB, nullable=True)              # {"mape": 0.12, "rmse": 450}

    is_active = Column(Boolean, default=False)          # Only one active per model_name

    trained_at = Column(DateTime, default=datetime.utcnow)
