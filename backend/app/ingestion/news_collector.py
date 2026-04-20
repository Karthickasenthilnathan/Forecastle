import random
from datetime import datetime

from app.ingestion.base import BaseCollector


class NewsCollector(BaseCollector):
    """Collects news sentiment signals for a product.

    In mock mode, generates realistic synthetic sentiment scores.
    In production, would integrate with NewsAPI or similar.
    """

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock

    def source_name(self) -> str:
        return "news"

    async def collect_data(self, product_id: int, date: datetime) -> dict:
        if self.use_mock:
            return self._mock_collect(product_id, date)

        # TODO: Real NewsAPI integration
        raise NotImplementedError("Real news collection not yet implemented")

    def _mock_collect(self, product_id: int, date: datetime) -> dict:
        # Simulate news sentiment: mostly neutral with occasional spikes
        base_sentiment = random.gauss(0.0, 0.15)

        # ~10% chance of a significant event
        if random.random() < 0.10:
            base_sentiment += random.choice([-1, 1]) * random.uniform(0.3, 0.7)

        sentiment = max(-1.0, min(1.0, round(base_sentiment, 3)))
        event_count = random.randint(0, 8)

        return {
            "signal_name": "news_sentiment",
            "signal_value": sentiment,
            "raw_payload": {
                "source": "mock_newsapi",
                "query": f"product_{product_id} supply demand",
                "event_count": event_count,
                "top_headline": "Simulated headline for demo",
                "collected_date": date.isoformat(),
            },
        }
