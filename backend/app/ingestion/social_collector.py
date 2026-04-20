import random
from datetime import datetime

from app.ingestion.base import BaseCollector


class SocialCollector(BaseCollector):
    """Collects social media trend signals for a product.

    In mock mode, generates synthetic mention counts and sentiment.
    In production, would integrate with Twitter/X API or similar.
    """

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock

    def source_name(self) -> str:
        return "social"

    async def collect_data(self, product_id: int, date: datetime) -> dict:
        if self.use_mock:
            return self._mock_collect(product_id, date)

        raise NotImplementedError("Real social collection not yet implemented")

    def _mock_collect(self, product_id: int, date: datetime) -> dict:
        # Base mention volume with weekly pattern (higher on weekdays)
        weekday = date.weekday()
        base_mentions = 120 if weekday < 5 else 60

        mentions = max(0, int(random.gauss(base_mentions, 30)))

        # Sentiment from mentions: correlated with volume spikes
        sentiment = random.gauss(0.05, 0.2)
        if mentions > base_mentions * 1.5:
            sentiment += 0.2  # Viral = positive buzz
        sentiment = max(-1.0, min(1.0, round(sentiment, 3)))

        return {
            "signal_name": "social_trend",
            "signal_value": sentiment,
            "raw_payload": {
                "source": "mock_twitter",
                "mention_count": mentions,
                "sentiment_score": sentiment,
                "trending": mentions > base_mentions * 1.5,
                "collected_date": date.isoformat(),
            },
        }
