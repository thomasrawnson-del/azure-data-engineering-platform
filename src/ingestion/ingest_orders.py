import pandas as pd

def load_orders(file_path: str) -> pd.DataFrame:
    """Load order data from a CSV file."""

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} orders")

    return df

if __name__ == "__main__":
    orders = load_orders("data/sample/orders.csv")

    print(orders.head())