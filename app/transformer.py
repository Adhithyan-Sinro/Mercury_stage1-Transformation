import pandas as pd
from datetime import datetime, timezone
from dateutil import parser
from app.schema_resolver import resolve_schema
from app.shop_resolver import resolve_shop_from_filename


REQUIRED_COLUMNS = {"sale_date"}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapped = {}
    for target, aliases in resolve_schema.items():
        for a in aliases:
            if a in df.columns:
                mapped[target] = a
                break
    # missing = [k for k in ["sale_date"] if k not in mapped]
    missing = REQUIRED_COLUMNS - mapped.keys()
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = pd.DataFrame(index=df.index)
    for target, source in mapped.items():
        out[target] = df[source]
    return out

# def parse_sale_date(df: pd.DataFrame) -> pd.DataFrame:
#     df["sale_date"] = df["sale_date"].apply(lambda x: parser.parse(str(x)).date())
#     return df

def parse_sale_date(df: pd.DataFrame) -> pd.DataFrame:
    def _parse(value):
        if pd.isna(value):
            return None
        return parser.parse(str(value), dayfirst=False).date()

    df["sale_date"] = df["sale_date"].apply(_parse)
    return df

def enrich(df: pd.DataFrame, *,filename: str, sender: str, file_id: str) -> pd.DataFrame:
    df["shop_id"] = resolve_shop_from_filename(filename)
    df["source_file_id"] = file_id
    df["source_sender"] = sender
    df["processing_timestamp"] = datetime.now(timezone.utc)
    return df


