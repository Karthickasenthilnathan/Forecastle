from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, ForeignKey
from app.models import Base

class Sales(Base):
    __tablename__ = "sales_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    date: Mapped[str] = mapped_column(Date)
    quantity: Mapped[int] = mapped_column(Integer)