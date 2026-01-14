from app.local_discovery import discover_local_files
from app.orchestrator import process_one_file

def run_stage2_local():
    files = discover_local_files()

    for file_ctx in files:
        process_one_file(file_ctx)

if __name__ == "__main__":
    run_stage2_local()
