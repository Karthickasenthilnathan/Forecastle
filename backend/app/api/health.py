from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import AsyncSessionLocal
from app.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    # --- Check database ---
    db_status = "disconnected"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception:
        pass

    # --- Check Redis ---
    redis_status = "disconnected"
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        if await r.ping():
            redis_status = "connected"
        await r.aclose()
    except Exception:
        pass

    overall = "ok" if db_status == "connected" else "degraded"

    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status,
    }