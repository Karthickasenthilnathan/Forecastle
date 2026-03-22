from fastapi import APIRouter
from app.api.products import router as products_router

api_router=APIRouter()
api_router.include_router(products_router,prefix='/api/v1')

from app.api.forecasts import router as forecasts_router
api_router.include_router(forecasts_router,prefix='/api/v1')