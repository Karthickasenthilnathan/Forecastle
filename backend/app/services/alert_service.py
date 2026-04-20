from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import AlertConfig, AlertHistory


async def check_alerts(
    product_id: int,
    forecast_data: dict,
    session: AsyncSession,
) -> list[dict]:
    """Compare forecast results against alert configs and create alert history entries.

    Args:
        product_id: The product being forecasted.
        forecast_data: Dict with keys like 'predictions', 'confidence', 'features'.
        session: Async DB session.

    Returns:
        List of triggered alert dicts.
    """
    result = await session.execute(
        select(AlertConfig).where(
            AlertConfig.product_id == product_id,
            AlertConfig.is_active == True,  # noqa: E712
        )
    )
    configs = result.scalars().all()

    if not configs:
        return []

    # Compute metrics from forecast
    predictions = forecast_data.get("predictions", [])
    confidence = forecast_data.get("confidence", 0.0)

    avg_qty = 0.0
    if predictions:
        avg_qty = sum(p.get("yhat", p.get("predicted_qty", 0)) for p in predictions) / len(predictions)

    metrics = {
        "confidence": confidence,
        "avg_predicted_qty": avg_qty,
        "deviation_pct": abs(1.0 - confidence) * 100,
        "stockout_risk": max(0, (1.0 - confidence) * 100),
    }

    triggered = []

    for config in configs:
        metric_value = metrics.get(config.metric)
        if metric_value is None:
            continue

        breached = False
        if config.direction == "above" and metric_value > config.threshold:
            breached = True
        elif config.direction == "below" and metric_value < config.threshold:
            breached = True

        if breached:
            message = (
                f"Alert: {config.metric} is {metric_value:.2f} "
                f"({config.direction} threshold of {config.threshold})"
            )

            alert = AlertHistory(
                config_id=config.id,
                product_id=product_id,
                metric_value=metric_value,
                message=message,
                is_read=False,
            )
            session.add(alert)

            triggered.append({
                "config_id": config.id,
                "metric": config.metric,
                "metric_value": metric_value,
                "threshold": config.threshold,
                "direction": config.direction,
                "message": message,
            })

    if triggered:
        await session.commit()

    return triggered


async def get_alerts(
    session: AsyncSession,
    unread_only: bool = False,
    limit: int = 50,
) -> list[AlertHistory]:
    """Get alert history, optionally filtered to unread only."""
    query = (
        select(AlertHistory)
        .order_by(AlertHistory.triggered_at.desc())
        .limit(limit)
    )
    if unread_only:
        query = query.where(AlertHistory.is_read == False)  # noqa: E712

    result = await session.execute(query)
    return result.scalars().all()


async def mark_alert_read(alert_id: int, session: AsyncSession) -> bool:
    """Mark a single alert as read. Returns True if found and updated."""
    result = await session.execute(
        select(AlertHistory).where(AlertHistory.id == alert_id)
    )
    alert = result.scalar_one_or_none()

    if not alert:
        return False

    alert.is_read = True
    await session.commit()
    return True
