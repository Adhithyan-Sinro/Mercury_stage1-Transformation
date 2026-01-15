import re
from app.shop_schema_config import SHOP_SCHEMAS

SHOP_REGEX_PATTERNS = [
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_\d{2}-\d{2}-\d{4}\.csv$",
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_\d{2}-\d{2}-\d{4}_\d{6}\.csv$",
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_@filenamedateformat\.xlsx$",
    r"^[a-f0-9]{64}_(?P<shop_id>sales report)\s+run\s+for\s+date\s+\d{2}-\d{2}-\d{4}\s+on\s+\d{2}\.\d{2}\.\d{4}\.\d{2}\.\d{2}\.xlsx$",
]

def normalize(raw: str) -> str:
    return (
        raw.strip()
           .lower()
           .replace(" ", "_")
           .replace("-", "_")
    )

def resolve_shop_from_filename(filename: str) -> str:
    name = filename.lower()

    for pattern in SHOP_REGEX_PATTERNS:
        match = re.search(pattern, name)
        if match:
            shop = normalize(match.group("shop_id"))

            if shop not in SHOP_SCHEMAS:
                raise ValueError(
                    f"UNKNOWN_SHOP_AFTER_PARSE: {shop} (from {filename})"
                )

            return shop

    raise ValueError(f"UNABLE_TO_RESOLVE_SHOP_FROM_FILENAME: {filename}")
