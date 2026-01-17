from dateutil import parser
import pandas as pd

def guard_non_empty(df):
    if df.empty:
        raise ValueError("NO_ROWS_AFTER_SCHEMA_MAPPING")


def guard_required_columns(df, required=("sale_date",)):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"MISSING_REQUIRED_COLUMNS: {missing}")


def guard_and_parse_sale_date(df):

    df = df[df["sale_date"].notna()].copy()
    raw = df["sale_date"]

    if raw.isnull().any():
        raise ValueError("SALE_DATE_NULL_BEFORE_PARSE")
    def _parse(value):
        try:
            return parser.parse(str(value), fuzzy=False).date()
        except Exception:
            raise ValueError(f"INVALID_SALES_DATE_VALUE: {value}")
        
    parsed = raw.apply(_parse)
    
    if parsed.isnull().any():
        raise ValueError("SALE_DATE_NULL_AFTER_PARSE")  

    df["sale_date"] = parsed
    return df

def guard_partition_count(df, max_partitions=5):
    if not df["sale_date"].map(type).eq(type(df["sale_date"].iloc[0])).all():
        raise ValueError("INCONSISTENT_SALE_DATE_TYPES")
    
    unique_dates = df["sale_date"].nunique()
    
    if unique_dates > max_partitions:
        raise ValueError(
            f"EXCESSIVE_PARTITIONS_IN_FILE: {unique_dates}"
        )
    