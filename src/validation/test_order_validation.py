import pandas as pd

from src.validation.order_validation import validate_orders


def test_invalid_orders_are_detected():

    data = {
        "order_id": [1, 1],
        "customer_id": ["C001", None],
        "order_date": ["2026-08-01", "not-a-date"],
        "product_id": ["P001", "P002"],
        "quantity": [1, -1],
        "unit_price": [10.0, None],
    }

    df = pd.DataFrame(data)

    valid, invalid = validate_orders(df)

    assert len(valid) == 0
    assert len(invalid) == 2