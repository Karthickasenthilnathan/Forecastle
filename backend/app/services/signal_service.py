from datetime import datetime, date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion import ALL_COLLECTORS
from app.models.signal import Signal


async def collect_signals(product_id: int, session: AsyncSession) -> list[dict]:
    """Run all signal collectors for a product and persist results to DB."""
    collected = []
    today = datetime.utcnow()

    for collector in ALL_COLLECTORS:
        try:
            result = await collector.collect_data(product_id, today)

            signal = Signal(
                product_id=product_id,
                date=today.date(),
                source=collector.source_name(),
                signal_name=result["signal_name"],
                signal_value=result["signal_value"],
                raw_payload=result.get("raw_payload"),
                collected_at=today,
            )
            session.add(signal)
            collected.append({
                "source": collector.source_name(),
                "signal_name": result["signal_name"],
                "signal_value": result["signal_value"],
                "status": "ok",
            })
        except Exception as e:
            collected.append({
                "source": collector.source_name(),
                "signal_name": None,
                "signal_value": None,
                "status": f"error: {str(e)}",
            })

    await session.commit()
    return collected


async def get_signals_for_product(
    product_id: int,
    session: AsyncSession,
    source: str | None = None,
    limit: int = 50,
) -> list[Signal]:
    """Get recent signals for a product, optionally filtered by source."""
    query = (
        select(Signal)
        .where(Signal.product_id == product_id)
        .order_by(Signal.collected_at.desc())
        .limit(limit)
    )
    if source:
        query = query.where(Signal.source == source)

    result = await session.execute(query)
    return result.scalars().all()


async def get_signal_health(session: AsyncSession) -> list[dict]:
    """Check the health of each signal source based on last collection time."""
    sources = ["news", "social", "weather", "supplier"]
    health = []

    for source_name in sources:
        result = await session.execute(
            select(
                func.max(Signal.collected_at).label("last_collected"),
                func.count(Signal.id).label("total_records"),
            ).where(Signal.source == source_name)
        )
        row = result.first()

        last_collected = row.last_collected if row else None
        total = row.total_records if row else 0

        # Consider unhealthy if no data or last collection > 24 hours ago
        status = "unknown"
        if last_collected:
            age_hours = (datetime.utcnow() - last_collected).total_seconds() / 3600
            status = "healthy" if age_hours < 24 else "stale"
        elif total == 0:
            status = "no_data"

        health.append({
            "source": source_name,
            "last_collected": last_collected.isoformat() if last_collected else None,
            "total_records": total,
            "status": status,
        })

    return health
