

from fastapi import APIRouter

from app.api import products, forecasts, signals, alerts, health

router = APIRouter(prefix="/api/v1")

router.include_router(products.router)
router.include_router(forecasts.router)
router.include_router(signals.router)
router.include_router(alerts.router)
router.include_router(health.router)