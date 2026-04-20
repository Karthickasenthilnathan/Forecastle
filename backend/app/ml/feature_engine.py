import pandas as pd
from sqlalchemy import select
from app.models.signal import Signal
from app.db.session import AsyncSessionLocal

async def generate_signal_features(product_id: int, lookback_days: int = 7):

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Signal).where(Signal.product_id == product_id)
        )

        signals = result.scalars().all()

        if not signals:
            return {
                "social": 0,
                "weather": 0
            }

        df = pd.DataFrame([
            {
                "date": s.date,
                "source": s.source,
                "value": s.signal_value
            }
            for s in signals
        ])

        # Filter recent window
        df["date"] = pd.to_datetime(df["date"])
        cutoff = df["date"].max() - pd.Timedelta(days=lookback_days)

        df = df[df["date"] >= cutoff]

        features = df.groupby("source")["value"].mean().to_dict()

        return {
            "social": features.get("social", 0),
            "weather": features.get("weather", 0)
        }