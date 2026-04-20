"""Celery tasks for periodic signal ingestion from external sources."""

import asyncio
from app.tasks.celery_app import celery_app


def _run_async(coro):
    """Helper to run async code inside synchronous Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.ingestion_tasks.collect_signals_for_product")
def collect_signals_for_product(product_id: int):
    """Collect all signals for a single product."""

    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.services.signal_service import collect_signals

        async with AsyncSessionLocal() as session:
            return await collect_signals(product_id, session)

    return _run_async(_run())


@celery_app.task(name="app.tasks.ingestion_tasks.collect_all_signals")
def collect_all_signals():
    """Periodic task: collect signals for all active products."""

    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.models.product import Product
        from app.services.signal_service import collect_signals
        from sqlalchemy import select

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Product))
            products = result.scalars().all()

            all_results = []
            for product in products:
                try:
                    collected = await collect_signals(product.id, session)
                    all_results.append({
                        "product_id": product.id,
                        "signals_collected": len(collected),
                        "status": "ok",
                    })
                except Exception as e:
                    all_results.append({
                        "product_id": product.id,
                        "status": f"error: {str(e)}",
                    })

            return {
                "products_processed": len(all_results),
                "results": all_results,
            }

    return _run_async(_run())
