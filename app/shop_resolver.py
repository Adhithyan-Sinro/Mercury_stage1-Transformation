import re

# Ordered list of patterns (first match wins)
SHOP_REGEX_PATTERNS = [
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_\d{2}-\d{2}-\d{4}\.csv$",      
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_\d{2}-\d{2}-\d{4}_\d{6}\.csv$",             
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_@filenamedateformat\.xlsx$",
    r"^[a-f0-9]{64}_(Sales report)\s+run\s+for\s+date\s+\d{2}-\d{2}-\d{4}\s+on\s+\d{2}\.\d{2}\.\d{4}\.\d{2}\.\d{2}\.xlsx$", 
    r"^[a-f0-9]{64}_(?P<shop_id>.+?)_\d{2}-\d{2}-\d{4}_\d{6}\.csv$"             
]

def resolve_shop_from_filename(filename: str) -> str:
    name = filename.lower()

    for pattern in SHOP_REGEX_PATTERNS:
        match = re.search(pattern, name)
        if match:
            raw = match.group("shop_id")
            normalized = (
                raw.strip()
                   .lower()
                   .replace(" ", "_")
                   .replace("-", "_")
                   )
            return f"shop_{normalized}"

    raise ValueError(f"Unable to resolve shop from filename: {filename}")
