from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.alert import AlertConfigCreate, AlertResponse, AlertHistoryResponse
from app.models.alert import AlertConfig
from app.services.alert_service import get_alerts, mark_alert_read

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
async def list_alerts(
    unread: bool = Query(False, description="Filter to unread alerts only"),
    session: AsyncSession = Depends(get_db),
):
    """Get alert history, optionally filtered to unread only."""
    alerts = await get_alerts(session, unread_only=unread)

    return {
        "count": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "config_id": a.config_id,
                "product_id": a.product_id,
                "message": a.message,
                "metric_value": a.metric_value,
                "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
                "is_read": a.is_read,
            }
            for a in alerts
        ],
    }


@router.post("/config", status_code=201)
async def create_alert_config(
    config: AlertConfigCreate,
    session: AsyncSession = Depends(get_db),
):
    """Create a new alert threshold configuration."""
    alert_config = AlertConfig(
        product_id=config.product_id,
        metric=config.metric,
        threshold=config.threshold,
        direction=config.direction,
        is_active=True,
    )

    session.add(alert_config)
    await session.commit()
    await session.refresh(alert_config)

    return {
        "config_id": alert_config.id,
        "product_id": alert_config.product_id,
        "metric": alert_config.metric,
        "threshold": alert_config.threshold,
        "direction": alert_config.direction,
        "message": "Alert config created successfully",
    }


@router.put("/{alert_id}/read", status_code=204)
async def mark_read(
    alert_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Mark an alert as read."""
    success = await mark_alert_read(alert_id, session)

    if not success:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")