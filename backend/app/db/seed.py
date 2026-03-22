from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models import Base
from app.models.product import Product
from app.models.sales import Sales
from datetime import date

DATABASE_URL = "postgresql://pulseflow:pulseflow_dev@localhost:5432/pulseflow"

engine = create_engine(DATABASE_URL)

def seed():
    with Session(engine) as session:
        # Create product
        product = Product(
            name="iPhone 15",
            sku="IPHONE15"
        )
        session.add(product)
        session.commit()

        # Add sales data
        sales_data = [
            Sales(product_id=product.id, date=date(2024, 1, 1), quantity=100),
            Sales(product_id=product.id, date=date(2024, 1, 2), quantity=120),
            Sales(product_id=product.id, date=date(2024, 1, 3), quantity=90),
        ]

        session.add_all(sales_data)
        session.commit()

        print("✅ Seed data inserted!")

if __name__ == "__main__":
    seed()