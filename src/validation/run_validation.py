import pandas as pd

from src.validation.order_validation import validate_orders


def run_validation(input_file: str) -> None:
    """Run data quality validation against an orders file."""

    print(f"Reading orders from: {input_file}")

    orders = pd.read_csv(input_file)

    print(f"Records received: {len(orders)}")

    valid_orders, invalid_orders = validate_orders(orders)

    print(f"Valid records: {len(valid_orders)}")
    print(f"Invalid records: {len(invalid_orders)}")

    
    valid_orders.to_csv(
    "data/processed/valid/orders_valid.csv",
    index=False,
    )

    invalid_orders.to_csv(
    "data/processed/quarantine/orders_invalid.csv",
    index=False,
    )

    print("\nValidation results written to:")
    print("  data/processed/valid/orders_valid.csv")
    print("  data/processed/quarantine/orders_invalid.csv")

    if len(invalid_orders) > 0:
        print("\nValidation errors:")

        for _, row in invalid_orders.iterrows():
            print(
                f"Order {row['order_id']}: "
                f"{row['validation_error']}"
            )


if __name__ == "__main__":

    run_validation(
        "data/sample/orders_with_errors.csv"
    )