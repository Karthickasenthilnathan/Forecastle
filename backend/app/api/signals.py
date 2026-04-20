from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.signal_service import (
    collect_signals,
    get_signals_for_product,
    get_signal_health,
)

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/{product_id}")
async def get_signals(
    product_id: int,
    source: str | None = Query(None, description="Filter by source: social, news, weather, supplier"),
    session: AsyncSession = Depends(get_db),
):
    """Get recent signals for a product, optionally filtered by source."""
    signals = await get_signals_for_product(product_id, session, source=source)

    return {
        "product_id": product_id,
        "count": len(signals),
        "signals": [
            {
                "id": s.id,
                "source": s.source,
                "signal_name": s.signal_name,
                "signal_value": s.signal_value,
                "date": str(s.date),
                "collected_at": s.collected_at.isoformat() if s.collected_at else None,
                "raw_payload": s.raw_payload,
            }
            for s in signals
        ],
    }


@router.post("/collect")
async def trigger_collect(
    product_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Trigger signal collection for a product from all sources."""
    results = await collect_signals(product_id, session)

    return {
        "product_id": product_id,
        "status": "completed",
        "sources_collected": len(results),
        "results": results,
    }


@router.get("/health/status")
async def signal_health(session: AsyncSession = Depends(get_db)):
    """Check the health status of all signal sources."""
    health = await get_signal_health(session)

    all_healthy = all(s["status"] == "healthy" for s in health)

    return {
        "overall": "healthy" if all_healthy else "degraded",
        "sources": health,
    }