from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.models import Base    # THIS is the key

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    sku: Mapped[str] = mapped_column(String)