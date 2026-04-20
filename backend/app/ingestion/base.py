from abc import ABC, abstractmethod
from datetime import datetime
class BaseCollector(ABC):
    @abstractmethod
    async def collect_data(self, product_id:int, date:datetime)->dict:
        pass
    @abstractmethod
    def source_name(self)->str:
        pass

