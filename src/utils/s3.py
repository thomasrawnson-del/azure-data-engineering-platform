import boto3
import pandas as pd
from io import BytesIO
from src.utils.config import load_config


def get_s3_client():
    """Create an S3 client using the configured AWS region."""

    config = load_config()

    return boto3.client(
        "s3",
        region_name=config["aws"]["region"],
    )


def create_data_lake_structure() -> None:
    """Create the initial data lake folder structure."""

    config = load_config()
    bucket_name = config["aws"]["bucket"]

    s3 = get_s3_client()

    folders = [
        "bronze/orders/",
        "silver/orders/",
        "quarantine/orders/",
        "gold/sales/",
    ]

    for folder in folders:
        s3.put_object(
            Bucket=bucket_name,
            Key=folder,
        )

        print(f"Created: s3://{bucket_name}/{folder}")


def upload_file(local_file: str, s3_key: str) -> None:
    """Upload a local file to S3."""

    config = load_config()
    bucket_name = config["aws"]["bucket"]

    s3 = get_s3_client()

    s3.upload_file(
        local_file,
        bucket_name,
        s3_key,
    )

    print(
        f"Uploaded {local_file} "
        f"to s3://{bucket_name}/{s3_key}"
    )

def upload_dataframe(
    df: pd.DataFrame,
    s3_key: str,
) -> None:
    """Upload a Pandas DataFrame as CSV to S3."""

    config = load_config()
    bucket_name = config["aws"]["bucket"]

    csv_buffer = BytesIO()

    df.to_csv(
        csv_buffer,
        index=False,
    )

    csv_buffer.seek(0)

    s3 = get_s3_client()

    s3.upload_fileobj(
        csv_buffer,
        bucket_name,
        s3_key,
    )

    print(
        f"Uploaded DataFrame to "
        f"s3://{bucket_name}/{s3_key}"
    )