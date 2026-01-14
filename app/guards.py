from dateutil import parser

def guard_non_empty(df):
    if df.empty:
        raise ValueError("NO_ROWS_AFTER_SCHEMA_MAPPING")


def guard_required_columns(df, required=("sale_date",)):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"MISSING_REQUIRED_COLUMNS: {missing}")


def guard_and_parse_sale_date(df):
    try:
        df["sale_date"] = df["sale_date"].apply(
            lambda x: parser.parse(str(x)).date()
        )
    except Exception as e:
        raise ValueError(f"SALE_DATE_PARSE_FAILED: {e}")

    if df["sale_date"].isnull().any():
        raise ValueError("SALE_DATE_NULL_AFTER_PARSE")

    return df


def guard_partition_count(df, max_partitions=5):
    if df["sale_date"].nunique() > max_partitions:
        raise ValueError(
            f"EXCESSIVE_PARTITIONS_IN_FILE: {df['sale_date'].nunique()}"
        )
