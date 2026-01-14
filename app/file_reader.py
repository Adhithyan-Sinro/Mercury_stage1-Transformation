import pandas as pd
from io import BytesIO

def read_file(bytes_data: bytes, filename: str, *, has_header: bool, delimiter=None):
    bio = BytesIO(bytes_data)
    name = filename.lower()

    header = 0 if has_header else None

    if name.endswith(".csv"):
        return pd.read_csv(bio, header=header, sep=delimiter)

    if name.endswith(".txt"):
        return pd.read_csv(bio, header=header, sep=delimiter)

    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(bio, header=header)

    if name.endswith(".ods"):
        return pd.read_excel(bio, header=header, engine="odf")

    raise ValueError(f"UNSUPPORTED_FILE_TYPE: {filename}")
