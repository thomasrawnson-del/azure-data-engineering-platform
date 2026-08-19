from datetime import datetime
from pathlib import Path

import dagster as dg

from src.gold.build_gold import build_sales_summary
from src.ingestion.ingest_orders import build_bronze_key, ingest_orders
from src.utils.config import load_config
from src.utils.s3 import download_dataframe, upload_dataframe
from src.validation.order_validation import validate_orders
from src.ai.quality_report import build_quality_report


def get_bronze_key() -> str:
    """Build the S3 key for today's Bronze orders file."""

    config = load_config()

    orders_file = config["data"]["orders_file"]
    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    file_name = Path(orders_file).name

    return build_bronze_key(
        ingestion_date,
        file_name,
    )


@dg.asset
def bronze_orders() -> None:
    """Ingest source orders into the Bronze S3 layer."""

    ingest_orders()


@dg.asset(
    deps=[bronze_orders],
)
def silver_orders() -> None:
    """Validate Bronze orders and write Silver and quarantine data."""

    bronze_key = get_bronze_key()

    orders = download_dataframe(bronze_key)

    valid_orders, invalid_orders = validate_orders(orders)

    silver_data = valid_orders.drop(
        columns=["validation_error"]
    )

    upload_dataframe(
        silver_data,
        "silver/orders/orders_valid.csv",
    )

    upload_dataframe(
        invalid_orders,
        "quarantine/orders/orders_invalid.csv",
    )


@dg.asset_check(asset=silver_orders)
def silver_orders_no_validation_errors() -> dg.AssetCheckResult:
    """Check that Silver contains no validation errors."""

    orders = download_dataframe(
        "silver/orders/orders_valid.csv"
    )

    passed = "validation_error" not in orders.columns

    return dg.AssetCheckResult(
        passed=bool(passed),
        metadata={
            "records_checked": len(orders),
        },
    )


@dg.asset_check(asset=silver_orders)
def silver_orders_unique_order_ids() -> dg.AssetCheckResult:
    """Check that Silver contains unique order IDs."""

    orders = download_dataframe(
        "silver/orders/orders_valid.csv"
    )

    duplicate_count = orders["order_id"].duplicated().sum()

    return dg.AssetCheckResult(
        passed=bool(duplicate_count == 0),
        metadata={
            "duplicate_order_ids": int(duplicate_count),
            "records_checked": len(orders),
        },
    )

@dg.asset_check(asset=silver_orders)
def silver_orders_positive_quantity() -> dg.AssetCheckResult:
    """Check that all Silver orders have a positive quantity."""

    orders = download_dataframe(
        "silver/orders/orders_valid.csv"
    )

    invalid_quantity_count = int(
        (orders["quantity"] <= 0).sum()
    )

    return dg.AssetCheckResult(
        passed=bool(invalid_quantity_count == 0),
        metadata={
            "invalid_quantity_records": invalid_quantity_count,
            "records_checked": len(orders),
        },
    )

@dg.asset_check(asset=silver_orders)
def silver_orders_valid_unit_prices() -> dg.AssetCheckResult:
    """Check that all Silver orders have valid unit prices."""

    orders = download_dataframe(
        "silver/orders/orders_valid.csv"
    )

    invalid_price_count = int(
        (
            orders["unit_price"].isna()
            | (orders["unit_price"] < 0)
        ).sum()
    )

    return dg.AssetCheckResult(
        passed=bool(invalid_price_count == 0),
        metadata={
            "invalid_price_records": invalid_price_count,
            "records_checked": len(orders),
        },
    )

@dg.asset(
    deps=[silver_orders],
)
def gold_sales() -> None:
    """Build the Gold sales dataset from Silver orders."""

    orders = download_dataframe(
        "silver/orders/orders_valid.csv"
    )

    gold = build_sales_summary(orders)

    upload_dataframe(
        gold,
        "gold/sales/daily_product_sales.csv",
    )

@dg.asset(
    deps=[silver_orders],
)
def ai_quality_report() -> None:
    """Analyse quarantined records and create a data quality report."""

    invalid_orders = download_dataframe(
        "quarantine/orders/orders_invalid.csv"
    )

    report = build_quality_report(invalid_orders)

    upload_dataframe(
        report,
        "gold/data_quality/quality_report.csv",
    )

daily_pipeline_schedule = dg.ScheduleDefinition(
    name="daily_pipeline_schedule",
    cron_schedule="0 6 * * *",
    target=dg.AssetSelection.all(),
)

defs = dg.Definitions(
    assets=[
        bronze_orders,
        silver_orders,
        ai_quality_report,
        gold_sales,
    ],
    asset_checks=[
        silver_orders_no_validation_errors,
        silver_orders_unique_order_ids,
        silver_orders_positive_quantity,
        silver_orders_valid_unit_prices,
    ],
    schedules=[
        daily_pipeline_schedule,
    ],
)

