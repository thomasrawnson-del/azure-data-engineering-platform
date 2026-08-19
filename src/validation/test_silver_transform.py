import pandas as pd

from src.validation.order_validation import validate_orders


def test_valid_orders_do_not_contain_validation_errors():
    df = pd.DataFrame(
        {
            "order_id": [10001],
            "customer_id": ["C001"],
            "order_date": ["2026-08-01"],
            "product_id": ["P100"],
            "quantity": [2],
            "unit_price": [25.0],
        }
    )

    valid_orders, invalid_orders = validate_orders(df)

    assert len(valid_orders) == 1
    assert len(invalid_orders) == 0

    silver_orders = valid_orders.drop(
        columns=["validation_error"]
    )

    assert "validation_error" not in silver_orders.columns