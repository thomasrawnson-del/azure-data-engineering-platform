import boto3

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


if __name__ == "__main__":
    create_data_lake_structure()

    upload_file(
        "data/sample/orders.csv",
        "bronze/orders/orders.csv",
    )