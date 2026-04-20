import random
import math
from datetime import datetime

from app.ingestion.base import BaseCollector


class WeatherCollector(BaseCollector):
    """Collects weather impact signals for a product.

    In mock mode, generates synthetic weather indices with seasonal patterns.
    In production, would integrate with OpenWeatherMap or similar.
    """

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock

    def source_name(self) -> str:
        return "weather"

    async def collect_data(self, product_id: int, date: datetime) -> dict:
        if self.use_mock:
            return self._mock_collect(product_id, date)

        raise NotImplementedError("Real weather collection not yet implemented")

    def _mock_collect(self, product_id: int, date: datetime) -> dict:
        day_of_year = date.timetuple().tm_yday

        # Seasonal temperature pattern (northern hemisphere)
        temp_base = 20 + 15 * math.sin(2 * math.pi * (day_of_year - 80) / 365)
        temperature = round(temp_base + random.gauss(0, 3), 1)

        # Weather impact on demand: extreme temps drive demand shifts
        # Normalized to [-1, 1]: negative = suppresses demand, positive = boosts
        deviation = (temperature - 20) / 20
        weather_impact = round(max(-1.0, min(1.0, deviation + random.gauss(0, 0.1))), 3)

        # Precipitation probability (higher in spring/fall)
        precip = random.random() < (0.3 + 0.2 * math.sin(2 * math.pi * day_of_year / 180))

        return {
            "signal_name": "weather_impact",
            "signal_value": weather_impact,
            "raw_payload": {
                "source": "mock_openweather",
                "temperature_c": temperature,
                "precipitation": precip,
                "weather_impact_index": weather_impact,
                "collected_date": date.isoformat(),
            },
        }
