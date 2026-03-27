import asyncio
import pandas as pd
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.models.product import Product
from app.models.sales import Sales


async def seed():
    async with AsyncSessionLocal() as db:

        # 🔹 Create products
        products = [
            Product(sku="P001", name="Product 1", category="Electronics"),
            Product(sku="P002", name="Product 2", category="Clothing"),
            Product(sku="P003", name="Product 3", category="Food"),
            Product(sku="P004", name="Product 4", category="Furniture"),
            Product(sku="P005", name="Product 5", category="Sports"),
        ]

        db.add_all(products)
        await db.commit()

        # 🔹 Load CSV
        df = pd.read_csv("synthetic_sales.csv")

        sales_data = []

        for _, row in df.iterrows():
            sales_data.append(
                Sales(
                    product_id=int(row["product_id"]),
                    date=pd.to_datetime(row["date"]).date(),
                    quantity=int(row["quantity"]),
                    revenue=float(row["quantity"] * 10),
                    channel="online",
                )
            )

        db.add_all(sales_data)
        await db.commit()

        print("✅ Seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed())