from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .product import Product
from .sales import Sales