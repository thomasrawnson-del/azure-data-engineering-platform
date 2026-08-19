import logging

from src.gold.build_gold import build_sales_summary
from src.ingestion.ingest_orders import ingest_orders
from src.utils.logging_config import configure_logging
from src.utils.s3 import (
    download_dataframe,
    upload_dataframe,
)
from src.validation.order_validation import validate_orders


logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    """Run the complete orders data pipeline."""

    logger.info("Starting data engineering pipeline")

    # --------------------------------------------------
    # 1. INGEST
    # --------------------------------------------------

    logger.info("Step 1/3: Ingestion")

    bronze_key = ingest_orders()

    logger.info(
        "Bronze ingestion complete: %s",
        bronze_key,
    )

    # --------------------------------------------------
    # 2. VALIDATE
    # --------------------------------------------------

    logger.info("Step 2/3: Validation")

    orders = download_dataframe(bronze_key)

    logger.info(
        "Loaded %d records from Bronze",
        len(orders),
    )

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

    # --------------------------------------------------
    # 3. GOLD
    # --------------------------------------------------

    logger.info("Step 3/3: Gold transformation")

    gold = build_sales_summary(silver_orders)

    upload_dataframe(
        gold,
        "gold/sales/daily_product_sales.csv",
    )

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    configure_logging()

    run_pipeline()