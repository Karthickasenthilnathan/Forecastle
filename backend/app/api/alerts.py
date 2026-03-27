from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
async def get_alerts():
    return {"alerts": []}


@router.post("/config")
async def create_alert_config():
    return {"message": "alert config created"}


@router.put("/{alert_id}/read")
async def mark_alert_read(alert_id: int):
    return {"message": f"alert {alert_id} marked as read"}