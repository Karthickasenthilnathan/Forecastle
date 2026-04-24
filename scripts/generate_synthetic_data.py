import pandas as pd
import numpy as np
from datetime import datetime


def generate_sales(product_id: int, days: int = 730):
    dates = pd.date_range(end=datetime.today(), periods=days)

    base = 500

    trend = np.linspace(0, 80, days)
    weekly = 50 * np.sin(2 * np.pi * np.arange(days) / 7)
    monthly = 30 * np.sin(2 * np.pi * np.arange(days) / 30)
    yearly = 120 * np.sin(2 * np.pi * np.arange(days) / 365)

    noise = np.random.normal(0, 40, days)

    # demand spikes
    shocks = np.zeros(days)
    for _ in range(np.random.randint(5, 8)):
        idx = np.random.randint(30, days - 30)
        shocks[idx:idx+5] += np.random.uniform(100, 300)

    quantity = base + trend + weekly + monthly + yearly + noise + shocks
    quantity = np.maximum(quantity, 0).astype(int)

    return pd.DataFrame({
        "date": dates,
        "product_id": product_id,
        "quantity": quantity
    })


if __name__ == "__main__":
    all_data = []

    for product_id in range(1, 6):  # 5 products
        df = generate_sales(product_id)
        all_data.append(df)

    final_df = pd.concat(all_data)

    final_df.to_csv("synthetic_sales.csv", index=False)
    print("✅ Data generated: synthetic_sales.csv")