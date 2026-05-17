import asyncio
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from sqlalchemy import func, select

from app.db.session import AsyncSessionLocal
from app.models.alert import AlertConfig, AlertHistory
from app.models.forecast import Forecast
from app.models.product import Product
from app.models.sales import Sales
from app.models.signal import Signal


PRODUCTS = [
    Product(id=1, sku="P001", name="Smart Thermostat Assembly", category="Electronics", unit="units"),
    Product(id=2, sku="P002", name="Insulated Field Jacket", category="Apparel", unit="units"),
    Product(id=3, sku="P003", name="Ready Meal Pack", category="Food", unit="cases"),
    Product(id=4, sku="P004", name="Modular Desk Frame", category="Furniture", unit="units"),
    Product(id=5, sku="P005", name="Training Recovery Kit", category="Sports", unit="kits"),
]

SIGNAL_PROFILES = {
    1: {"social": 0.18, "weather": -0.06, "news": 0.11, "supplier": -0.08},
    2: {"social": 0.09, "weather": 0.14, "news": 0.04, "supplier": -0.05},
    3: {"social": 0.06, "weather": 0.08, "news": 0.12, "supplier": -0.03},
    4: {"social": -0.02, "weather": 0.03, "news": 0.07, "supplier": -0.12},
    5: {"social": 0.16, "weather": 0.05, "news": 0.09, "supplier": -0.04},
}


def _sales_csv_path() -> Path:
    return Path(__file__).resolve().parents[2] / "synthetic_sales.csv"


async def _table_count(db, model) -> int:
    result = await db.execute(select(func.count()).select_from(model))
    return result.scalar_one()


async def _seed_products(db) -> None:
    existing = await db.execute(select(Product))
    products_by_sku = {product.sku: product for product in existing.scalars().all()}

    for product in PRODUCTS:
        current = products_by_sku.get(product.sku)
        if current:
            current.name = product.name
            current.category = product.category
            current.unit = product.unit
        else:
            db.add(product)

    await db.commit()


async def _seed_sales(db) -> None:
    if await _table_count(db, Sales):
        return

    df = pd.read_csv(_sales_csv_path())
    sales_data = [
        Sales(
            product_id=int(row["product_id"]),
            date=pd.to_datetime(row["date"]).date(),
            quantity=int(row["quantity"]),
            revenue=float(row["quantity"] * 10),
            channel="online",
        )
        for _, row in df.iterrows()
    ]

    db.add_all(sales_data)
    await db.commit()


async def _seed_signals(db) -> None:
    today = date.today()
    collected_at = datetime.utcnow()
    rows = []

    for product in PRODUCTS:
        for source, value in SIGNAL_PROFILES[product.id].items():
            existing = await db.execute(
                select(Signal).where(
                    Signal.product_id == product.id,
                    Signal.source == source,
                    Signal.signal_name == f"{source}_impact_score",
                )
            )
            if existing.scalar_one_or_none():
                continue

            rows.append(
                Signal(
                    product_id=product.id,
                    date=today,
                    source=source,
                    signal_name=f"{source}_impact_score",
                    signal_value=value,
                    raw_payload={
                        "source": "seeded_from_synthetic_sales",
                        "description": "Dashboard-ready signal derived for local development",
                    },
                    collected_at=collected_at,
                )
            )

    if rows:
        db.add_all(rows)
        await db.commit()


async def _seed_forecasts(db) -> None:
    df = pd.read_csv(_sales_csv_path())
    df["date"] = pd.to_datetime(df["date"])
    generated_at = datetime.utcnow()
    forecast_rows = []

    for product in PRODUCTS:
        product_sales = df[df["product_id"] == product.id].sort_values("date")
        recent = product_sales.tail(28)["quantity"]
        baseline = float(recent.mean())
        volatility = float(recent.std() or baseline * 0.08)
        contributions = SIGNAL_PROFILES[product.id]
        signal_lift = sum(contributions.values())

        for horizon in (2, 4, 8):
            existing = await db.execute(
                select(func.count())
                .select_from(Forecast)
                .where(Forecast.product_id == product.id, Forecast.horizon_weeks == horizon)
            )
            if existing.scalar_one() >= horizon * 7:
                continue

            for day in range(1, horizon * 7 + 1):
                weekly_seasonality = 1 + 0.06 * ((day % 7) - 3) / 3
                trend = 1 + day * 0.004
                predicted = baseline * weekly_seasonality * trend * (1 + signal_lift)
                lower = max(predicted - volatility * 0.9, 0)
                upper = predicted + volatility * 1.1

                forecast_rows.append(
                    Forecast(
                        product_id=product.id,
                        forecast_date=date.today() + timedelta(days=day),
                        generated_at=generated_at,
                        horizon_weeks=horizon,
                        predicted_qty=round(predicted, 2),
                        lower_bound=round(lower, 2),
                        upper_bound=round(upper, 2),
                        confidence=0.86 if horizon == 2 else 0.83 if horizon == 4 else 0.78,
                        model_version="seeded-prophet-xgb-v1",
                        explanation=(
                            "Forecast generated from recent synthetic sales history and persisted "
                            "signal impacts for the dashboard."
                        ),
                        signal_contributions=contributions,
                    )
                )

    if forecast_rows:
        db.add_all(forecast_rows)
        await db.commit()


async def _seed_alerts(db) -> None:
    result = await db.execute(
        select(AlertConfig).where(
            AlertConfig.product_id == 1,
            AlertConfig.metric == "deviation_pct",
        )
    )
    config = result.scalar_one_or_none()
    if not config:
        config = AlertConfig(
            product_id=1,
            metric="deviation_pct",
            threshold=10.0,
            direction="above",
            is_active=True,
        )
        db.add(config)
        await db.flush()

    result = await db.execute(
        select(AlertHistory).where(
            AlertHistory.config_id == config.id,
            AlertHistory.is_read == False,  # noqa: E712
        )
    )
    if not result.scalar_one_or_none():
        db.add(
            AlertHistory(
                config_id=config.id,
                product_id=1,
                metric_value=12.4,
                message="Forecast variance is above 12% for Smart Thermostat Assembly.",
                is_read=False,
            )
        )

    await db.commit()


async def seed():
    async with AsyncSessionLocal() as db:
        await _seed_products(db)
        await _seed_sales(db)
        await _seed_signals(db)
        await _seed_forecasts(db)
        await _seed_alerts(db)

        print("Seeding completed with products, sales, forecasts, signals, and alerts.")


if __name__ == "__main__":
    asyncio.run(seed())
