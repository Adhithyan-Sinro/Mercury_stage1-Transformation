from pathlib import Path
import hashlib
from app.local_file_ctx import LocalFileCtx

def discover_local_files(base_path="C:/Users/user/Documents/NESA/Mercury/Mercury-ETL -Pipeline-AWS/local_test"):
    files = []

    for path in Path(base_path).glob("*"):
        if not path.is_file():
            continue

        data = path.read_bytes()
        file_id = hashlib.sha256(data).hexdigest()

        files.append(
            LocalFileCtx(
                file_id=file_id,
                filename=path.name,
                bytes=data,
            )
        )

    return files
