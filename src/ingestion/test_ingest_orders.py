from src.ingestion.ingest_orders import build_bronze_key


def test_build_bronze_key():
    result = build_bronze_key(
        "2026-08-18",
        "orders.csv",
    )

    assert result == (
        "bronze/orders/"
        "ingestion_date=2026-08-18/"
        "orders.csv"
    )