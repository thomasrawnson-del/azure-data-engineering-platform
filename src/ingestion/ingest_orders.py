import logging
import pandas as pd
from src.utils.config import load_config
from src.utils.logging_config import configure_logging


logger = logging.getLogger(__name__)


def load_orders(file_path: str) -> pd.DataFrame:
    """Load order data from a CSV file."""

    logger.info("Loading orders from %s", file_path)

    try:
        df = pd.read_csv(file_path)

    except FileNotFoundError:
        logger.error("Orders file not found: %s", file_path)
        raise

    except Exception:
        logger.exception("Unexpected error loading orders")
        raise

    logger.info("Loaded %d orders", len(df))

    return df


if __name__ == "__main__":
    configure_logging()

    config = load_config()

    orders_file = config["data"]["orders_file"]

    orders = load_orders(orders_file)

    print(orders.head())