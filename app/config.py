import os
from dotenv import load_dotenv

load_dotenv()

RAW_BUCKET = os.getenv("RAW_BUCKET_NAME")
CURATED_BUCKET = os.getenv("CURATED_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
METADATA_TABLE = os.getenv("METADATA_TABLE")

# How many ingestion days to scan for late files
RAW_LOOKBACK_DAYS = int(os.getenv("RAW_LOOKBACK_DAYS", "7"))


LOCAL_MODE = True
LOCAL_OUTPUT_DIR = "local_curated_output"
