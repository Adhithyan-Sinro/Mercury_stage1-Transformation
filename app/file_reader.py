import pandas as pd
from io import BytesIO
import chardet


def detect_encoding(data: bytes) -> str:
    result = chardet.detect(data)
    return result['encoding'] or 'utf-8'

def read_file(bytes_data: bytes, filename: str, *, has_header: bool, delimiter=None):
    bio = BytesIO(bytes_data)
    name = filename.lower()
    header = 0 if has_header else None

    if name.endswith((".csv", ".txt")):
        encoding = detect_encoding(bytes_data)

        return pd.read_csv(
            bio,
            header=header,
            sep=delimiter,
            encoding=encoding,
        )

    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(bio, header=header)

    if name.endswith(".ods"):
        return pd.read_excel(bio, header=header, engine="odf")

    raise ValueError(f"UNSUPPORTED_FILE_TYPE: {filename}")

