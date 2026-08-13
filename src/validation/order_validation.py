import pandas as pd


def validate_orders(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate order data and separate valid and invalid records.
    """

    errors = pd.Series("", index=df.index, dtype="object")

    # Check for duplicate order IDs
    duplicate_orders = df["order_id"].duplicated(keep=False)

    errors.loc[duplicate_orders] += "Duplicate order ID; "

    # Check customer IDs
    missing_customer = df["customer_id"].isna() | (
        df["customer_id"].astype(str).str.strip() == ""
    )

    errors.loc[missing_customer] += "Missing customer ID; "

    # Check quantity
    invalid_quantity = df["quantity"] <= 0

    errors.loc[invalid_quantity] += "Quantity must be greater than zero; "

    # Check dates
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")

    invalid_dates = parsed_dates.isna()

    errors.loc[invalid_dates] += "Invalid order date; "

    # Check unit price
    missing_price = df["unit_price"].isna()

    errors.loc[missing_price] += "Missing unit price; "

    df = df.copy()

    df["validation_error"] = errors

    valid_orders = df[df["validation_error"] == ""].copy()

    invalid_orders = df[df["validation_error"] != ""].copy()

    return valid_orders, invalid_orders