import pandas as pd

from src.gold.build_gold import build_sales_summary


def test_build_sales_summary():

    df = pd.DataFrame(
        {
            "order_id": [10001, 10002],
            "customer_id": ["C001", "C002"],
            "order_date": [
                "2026-08-01",
                "2026-08-01",
            ],
            "product_id": [
                "P100",
                "P100",
            ],
            "quantity": [2, 3],
            "unit_price": [25.0, 25.0],
        }
    )

    result = build_sales_summary(df)

    assert len(result) == 1

    row = result.iloc[0]

    assert row["product_id"] == "P100"
    assert row["total_orders"] == 2
    assert row["total_quantity"] == 5
    assert row["total_sales"] == 125.0