import pandas as pd

from src.utils.config import load_config
from src.utils.s3 import (
    download_dataframe,
    upload_dataframe,
)


def build_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create a business-ready sales summary from Silver orders."""

    sales = df.copy()

    sales["order_date"] = pd.to_datetime(
        sales["order_date"]
    )

    sales["sales_value"] = (
        sales["quantity"] * sales["unit_price"]
    )

    summary = (
        sales.groupby(
            ["order_date", "product_id"],
            as_index=False,
        )
        .agg(
            total_orders=("order_id", "count"),
            total_quantity=("quantity", "sum"),
            total_sales=("sales_value", "sum"),
        )
    )

    return summary


def build_gold() -> None:
    """Read Silver data and create the Gold sales dataset."""

    config = load_config()

    silver_key = "silver/orders/orders_valid.csv"

    orders = download_dataframe(silver_key)

    gold = build_sales_summary(orders)

    upload_dataframe(
        gold,
        "gold/sales/daily_product_sales.csv",
    )

    print(
        "Gold sales dataset created successfully"
    )


if __name__ == "__main__":
    build_gold()