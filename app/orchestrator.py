import logging
from app.file_reader import read_file
from app.schema_resolver import resolve_schema
from app.shop_resolver import resolve_shop_from_filename
from app.shop_schema_config import SHOP_SCHEMAS
from app.guards import (
    guard_non_empty,
    guard_required_columns,
    guard_and_parse_sale_date,
    guard_partition_count,
)
from app.writer import write_partitions
from app.metadata import mark_stage2_success, mark_stage2_failed

logger = logging.getLogger(__name__)


def process_one_file(file_ctx):
    """
    file_ctx contains:
      - file_id
      - filename
      - bytes
    """
    try:
        # 1. Resolve shop
        shop_id = resolve_shop_from_filename(file_ctx.filename)

        # 2. Load schema contract
        schema = SHOP_SCHEMAS[shop_id]

        # 3. Read raw file
        df_raw = read_file(
            bytes_data=file_ctx.bytes,
            filename=file_ctx.filename,
            has_header=schema["has_header"],
            delimiter=schema.get("delimiter"),
        )

        # 4. Apply schema mapping
        df = resolve_schema(df_raw, shop_id=shop_id)

        # 5. Guardrails (STRICT)
        guard_non_empty(df)
        guard_required_columns(df)
        df = guard_and_parse_sale_date(df)
        guard_partition_count(df)

        # 6. Enrichment
        df["shop_id"] = shop_id
        df["source_file_id"] = file_ctx.file_id

        # 7. Write curated partitions
        write_partitions(df)

        # 8. Mark success
        mark_stage2_success(file_ctx.file_id)

    except Exception as e:
        logger.error(
            "STAGE2_FILE_FAILED",
            extra={
                "file_id": file_ctx.file_id,
                "source_filename": file_ctx.filename,
                "error": str(e),
            },
        )
        mark_stage2_failed(file_ctx.file_id, str(e))
