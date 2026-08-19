from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils.config import load_config
from src.utils.s3 import upload_file


def load_orders(file_path: str) -> pd.DataFrame:
    """Load order data from a CSV file."""

    print(f"Loading orders from {file_path}")

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} orders")

    return df


def build_bronze_key(
    ingestion_date: str,
    file_name: str,
) -> str:
    """Build the S3 object key for Bronze data."""

    return (
        f"bronze/orders/"
        f"ingestion_date={ingestion_date}/"
        f"{file_name}"
    )


def ingest_orders() -> str:
    """Load orders and upload the source file to S3 Bronze."""

    config = load_config()

    orders_file = config["data"]["orders_file"]

    ingestion_date = datetime.now().strftime("%Y-%m-%d")

    file_name = Path(orders_file).name

    bronze_key = build_bronze_key(
        ingestion_date,
        file_name,
    )

    load_orders(orders_file)

    upload_file(
        orders_file,
        bronze_key,
    )

    print(
        f"Bronze ingestion complete: "
        f"s3://{config['aws']['bucket']}/{bronze_key}"
    )
    
    return bronze_key


if __name__ == "__main__":
    ingest_orders()