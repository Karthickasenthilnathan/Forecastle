from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, ForeignKey
from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy import UniqueConstraint

class Sales(Base):
    __tablename__ = "sales_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    date: Mapped[str] = mapped_column(Date)
    quantity: Mapped[int] = mapped_column(Integer)

    revenue=Column(Integer,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow())
    channel = Column(String(50), nullable=True)
    __table_args__ = (
        UniqueConstraint("product_id", "date", "channel", name="unique_sales_entry"),
    )


