from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.models import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

    # NEW FIELDS 
    category = Column(String(100), nullable=True)
    unit = Column(String(20), default="units")

    created_at = Column(DateTime, default=datetime.utcnow)