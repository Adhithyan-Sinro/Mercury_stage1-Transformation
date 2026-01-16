import pandas as pd
from datetime import datetime, timezone


def enrich(
    df: pd.DataFrame,
    *,
    shop_id: str,
    sender: str,
    file_id: str,
) -> pd.DataFrame:
    df["shop_id"] = shop_id
    df["source_file_id"] = file_id
    df["source_sender"] = sender
    df["processing_timestamp"] = datetime.now(timezone.utc)
    return df


def aggregate_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales amount per shop per day.
    """

    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    grouped = (
        df
        .groupby(["shop_id", "sale_date"], as_index=False)
        .agg(
            total_amount=("amount", "sum"),
            record_count=("amount", "count"),
        )
    )

    return grouped
