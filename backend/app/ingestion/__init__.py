from app.ingestion.news_collector import NewsCollector
from app.ingestion.social_collector import SocialCollector
from app.ingestion.weather_collector import WeatherCollector
from app.ingestion.supplier_collector import SupplierCollector

ALL_COLLECTORS = [
    NewsCollector(),
    SocialCollector(),
    WeatherCollector(),
    SupplierCollector(),
]
