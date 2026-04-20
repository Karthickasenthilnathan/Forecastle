"""Celery tasks for forecast generation and model retraining."""

import asyncio
from app.tasks.celery_app import celery_app


def _run_async(coro):
    """Helper to run async code inside synchronous Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.forecast_tasks.generate_forecast_task")
def generate_forecast_task(product_id: int, horizon_weeks: int = 4):
    """Generate forecast for a single product (async-wrapped)."""

    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.services.forecast_service import generate_forecast

        async with AsyncSessionLocal() as session:
            result = await generate_forecast(product_id, horizon_weeks, session)
            return {
                "product_id": product_id,
                "predictions_count": len(result.get("predictions", [])),
                "confidence": result.get("confidence"),
            }

    return _run_async(_run())


@celery_app.task(name="app.tasks.forecast_tasks.scheduled_retrain")
def scheduled_retrain():
    """Weekly scheduled task: regenerate forecasts for all active products."""

    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.models.product import Product
        from app.services.forecast_service import generate_forecast
        from sqlalchemy import select

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Product))
            products = result.scalars().all()

            results = []
            for product in products:
                try:
                    forecast = await generate_forecast(product.id, 4, session)
                    results.append({
                        "product_id": product.id,
                        "status": "ok",
                        "predictions": len(forecast.get("predictions", [])),
                    })
                except Exception as e:
                    results.append({
                        "product_id": product.id,
                        "status": f"error: {str(e)}",
                    })

            return {"retrained": len(results), "results": results}

    return _run_async(_run())
