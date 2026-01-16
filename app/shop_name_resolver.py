import re
from app.shop_schema_config import SHOP_SCHEMAS
from datetime import datetime   
from pathlib import Path

FILENAME_SHOP_ALIASES = {
    "sales report run for date": "guess",
}

def normalize(raw: str) -> str:
    return (
        raw.strip()
           .lower()
           .replace(" ", "_")
           .replace("-", "_")
    )

def is_date_token(tokens):
    joined = "_".join(tokens)
    for fmt in ("%d-%m-%Y", "%d_%m_%Y"):
        try:
            datetime.strptime(joined, fmt)
            return True
        except ValueError:
            pass
    return False


def resolve_shop_from_filename(filename: str) -> str:
    name = Path(filename).stem.lower()

    # 1. Alias-based override (highest priority)
    for phrase, shop in FILENAME_SHOP_ALIASES.items():
        if phrase in name:
            if shop not in SHOP_SCHEMAS:
                raise ValueError(
                    f"ALIAS_SHOP_NOT_IN_SCHEMA: {shop} (from {filename})"
                )
            return shop

    # 2. Normal semantic parsing (date-aware logic)
    parts = name.split("_")

    if len(parts) < 3:
        raise ValueError(f"INVALID_FILENAME_FORMAT: {filename}")

    # Detect date from right
    date_start_idx = None
    for i in range(len(parts) - 1, 0, -1):
        try:
            datetime.strptime("_".join(parts[i:]), "%d_%m_%Y")
            date_start_idx = i
            break
        except ValueError:
            try:
                datetime.strptime("_".join(parts[i:]), "%d-%m-%Y")
                date_start_idx = i
                break
            except ValueError:
                pass

    if date_start_idx is None:
        raise ValueError(f"NO_DATE_FOUND_IN_FILENAME: {filename}")

    shop_raw = "_".join(parts[1:date_start_idx])
    shop_id = normalize(shop_raw)

    if shop_id not in SHOP_SCHEMAS:
        raise ValueError(
            f"UNKNOWN_SHOP_AFTER_PARSE: {shop_id} (from {filename})"
        )

    return shop_id