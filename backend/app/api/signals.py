from fastapi import APIRouter

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/{product_id}")
async def get_signals(product_id: int):
    return {
        "product_id": product_id,
        "signals": []
    }


@router.post("/collect")
async def collect_signals():
    return {"status": "collecting signals..."}


@router.get("/health")
async def signal_health():
    return {"status": "all signal sources healthy"}