import pandas as pd

from src.utils.config import load_config


def load_orders(file_path: str) -> pd.DataFrame:
    """Load order data from a CSV file."""

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} orders")

    return df


if __name__ == "__main__":
    config = load_config()

    orders_file = config["data"]["orders_file"]

    print(f"Loading orders from: {orders_file}")

    orders = load_orders(orders_file)

    print(orders.head())