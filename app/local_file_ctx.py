from dataclasses import dataclass
from pathlib import Path

@dataclass
class LocalFileCtx:
    file_id: str
    filename: str
    bytes: bytes
