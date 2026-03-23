from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .product import Product
from .sales import Sales
from .signal import Signal
from .forecast import Forecast
from .alert import AlertConfig, AlertHistory
