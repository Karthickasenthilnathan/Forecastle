import random
from datetime import datetime

from app.ingestion.base import BaseCollector


class SupplierCollector(BaseCollector):
    """Collects supplier lead-time signals for a product.

    In mock mode, generates synthetic lead-time ratios.
    In production, would integrate with ERP/supplier APIs.
    """

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock

    def source_name(self) -> str:
        return "supplier"

    async def collect_data(self, product_id: int, date: datetime) -> dict:
        if self.use_mock:
            return self._mock_collect(product_id, date)

        raise NotImplementedError("Real supplier collection not yet implemented")

    def _mock_collect(self, product_id: int, date: datetime) -> dict:
        # Normal lead time: 7 days. Ratio = actual / expected.
        # 1.0 = on time, >1.0 = delayed, <1.0 = early
        expected_days = 7
        actual_days = max(1, int(random.gauss(expected_days, 2)))

        # ~5% chance of a supply disruption
        if random.random() < 0.05:
            actual_days += random.randint(5, 14)

        lead_time_ratio = round(actual_days / expected_days, 3)

        # Signal value: deviation from 1.0 (negative = risk)
        signal_value = round(1.0 - lead_time_ratio, 3)

        return {
            "signal_name": "supplier_lead_time",
            "signal_value": signal_value,
            "raw_payload": {
                "source": "mock_erp",
                "expected_days": expected_days,
                "actual_days": actual_days,
                "lead_time_ratio": lead_time_ratio,
                "disruption_flag": actual_days > expected_days * 2,
                "collected_date": date.isoformat(),
            },
        }
