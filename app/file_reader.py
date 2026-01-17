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

        first_line = bytes_data.split(b'\n', 1)[0].decode(encoding, errors='ignore').strip()
        skiprows = None
        
        if first_line.lower().startswith('sep='):
            skiprows = [0]  # Skip the first row
            # Extract delimiter from the sep= line if not provided
            if delimiter is None:
                delimiter = first_line.split('=', 1)[1].strip()

        return pd.read_csv(
            bio,
            header=header,
            sep=delimiter,
            encoding=encoding,
            skiprows=skiprows,
        )

    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(bio, header=header)

    if name.endswith(".ods"):
        return pd.read_excel(bio, header=header, engine="odf")

    raise ValueError(f"UNSUPPORTED_FILE_TYPE: {filename}")

