import logging
from app.local_discovery import discover_local_files
from app.orchestrator import process_one_file

def run_stage2_local():
    files = discover_local_files()

    logging.info("Discovered %d files for Stage-2", len(files))

    for file_ctx in files:
        logging.info(
            "Processing file",
            extra={
                "file_id": file_ctx.file_id,
                "source_filename": file_ctx.filename
            }
        )
        process_one_file(file_ctx)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    run_stage2_local()
