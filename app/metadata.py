import boto3
from datetime import datetime, timezone
from app.config import METADATA_TABLE, AWS_REGION

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(METADATA_TABLE)


def mark_stage2_success(file_id: str):
    table.update_item(
        Key={"file_id": file_id},
        UpdateExpression="""
            SET stage2_status = :status,
                stage2_processed_at = :ts
        """,
        ExpressionAttributeValues={
            ":status": "SUCCESS",
            ":ts": datetime.now(timezone.utc).isoformat(),
        },
    )


def mark_stage2_failed(file_id: str, reason: str):
    table.update_item(
        Key={"file_id": file_id},
        UpdateExpression="""
            SET stage2_status = :status,
                stage2_processed_at = :ts,
                stage2_error_reason = :reason
        """,
        ExpressionAttributeValues={
            ":status": "FAILED",
            ":ts": datetime.now(timezone.utc).isoformat(),
            ":reason": reason[:500],  # prevent oversized items
        },
    )
