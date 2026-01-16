import logging
from app.file_reader import read_file
from app.schema_resolver import resolve_schema
from app.shop_name_resolver import resolve_shop_from_filename
from app.shop_schema_config import SHOP_SCHEMAS
from app.guards import (
    guard_non_empty,
    guard_required_columns,
    guard_and_parse_sale_date,
    guard_partition_count,
)
from app.writer import write_partitions
from app.metadata import mark_stage2_success, mark_stage2_failed
from app.transformer import aggregate_daily_sales

logger = logging.getLogger(__name__)


def process_one_file(file_ctx):
   
    logger.info(
    "STAGE2_PROCESSING_FILE",
    extra={
        "file_id": file_ctx.file_id,
        "source_filename": file_ctx.filename,
        },
    )
    

    try:
        # 1. Resolve shop
        shop_id = resolve_shop_from_filename(file_ctx.filename)

        # 2. Load schema contract
        
        if shop_id not in SHOP_SCHEMAS:
            raise ValueError(f"NO_SCHEMA_DEFINED_FOR_SHOP: {shop_id}")


        # 3. Read raw file
        df_raw = read_file(
            bytes_data=file_ctx.bytes,
            filename=file_ctx.filename,
            has_header=SHOP_SCHEMAS[shop_id]["has_header"],
            delimiter=SHOP_SCHEMAS[shop_id].get("delimiter"),
        )

        # 4. Apply schema mapping
        df = resolve_schema(df_raw, shop_id=shop_id)

        # 5. Guardrails 
        guard_non_empty(df)
        guard_required_columns(df, required=("sale_date", "amount"))

        logger.info(
            "Parsing sale_date",
            extra={
                "file_id": file_ctx.file_id, 
                "shop_id": shop_id,
                "rows": len(df)
                },
        )

        df = guard_and_parse_sale_date(df)       

        # 6. Enrichment
        df["shop_id"] = shop_id
        df["source_file_id"] = file_ctx.file_id

        # 7. Transformation - aggregation
        df_transformed = aggregate_daily_sales(df)

        #8 Post-Transform guard
        guard_partition_count(df_transformed)

        #9 Write
        write_partitions(
            df_transformed,
            source_file_id=file_ctx.file_id,
            shop_id=shop_id
            )

        #8. Log success

        logger.info(
            "STAGE2_FILE_SUCCESS",
            extra={
                "file_id": file_ctx.file_id,
                "source_filename": file_ctx.filename,
                "shop_id": shop_id,
                "rows": len(df_transformed),
            },
        )
        
        # 9. Mark success
        mark_stage2_success(file_ctx.file_id)

    except Exception as e:
        logger.exception(
            "STAGE2_FILE_FAILED",
            extra={
                "file_id": file_ctx.file_id,
                "source_filename": file_ctx.filename,
                "error": str(e),
            },
        )
        mark_stage2_failed(file_ctx.file_id, str(e))
