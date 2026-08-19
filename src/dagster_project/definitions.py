import dagster as dg

from src.gold.build_gold import build_sales_summary
from src.ingestion.ingest_orders import ingest_orders
from src.utils.s3 import download_dataframe, upload_dataframe
from src.validation.order_validation import validate_orders


@dg.asset
def bronze_orders() -> str:
    """Ingest source orders into the Bronze S3 layer."""

    bronze_key = ingest_orders()

    return bronze_key


@dg.asset
def silver_orders(bronze_orders: str) -> str:
    """Validate Bronze orders and write valid records to Silver."""

    orders = download_dataframe(bronze_orders)

    valid_orders, invalid_orders = validate_orders(orders)

    silver_orders = valid_orders.drop(
        columns=["validation_error"]
    )

    upload_dataframe(
        silver_orders,
        "silver/orders/orders_valid.csv",
    )

    upload_dataframe(
        invalid_orders,
        "quarantine/orders/orders_invalid.csv",
    )

    return "silver/orders/orders_valid.csv"


@dg.asset
def gold_sales(silver_orders: str) -> str:
    """Build the Gold sales dataset from Silver orders."""

    orders = download_dataframe(silver_orders)

    gold = build_sales_summary(orders)

    upload_dataframe(
        gold,
        "gold/sales/daily_product_sales.csv",
    )

    return "gold/sales/daily_product_sales.csv"


defs = dg.Definitions(
    assets=[
        bronze_orders,
        silver_orders,
        gold_sales,
    ],
)