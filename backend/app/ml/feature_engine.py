import random


def generate_signal_features(product_id: int):
    """
    Mock signal features (we'll replace with real signals later)
    """

    return {
        "sentiment_score": random.uniform(-1, 1),
        "weather_index": random.uniform(0, 1),
        "trend_strength": random.uniform(0, 1),
        "supply_risk": random.uniform(0, 1),
    }