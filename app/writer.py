from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from io import BytesIO
from app.config import LOCAL_MODE, AWS_REGION, CURATED_BUCKET

s3 = boto3.client("s3", region_name=AWS_REGION)

def write_partitions(df, *, source_file_id: str, shop_id: str):
    if LOCAL_MODE:
        write_partitions_local(
            df, 
            source_file_id=source_file_id,
            shop_id=shop_id
            )
    else:
        write_partitions_s3(
            df, 
            source_file_id=source_file_id,
            shop_id=shop_id
            )

def write_partitions_local(df, *, source_file_id: str):
    base = Path("local_curated_output")

    for sale_date, group in df.groupby("sale_date"):
        year = sale_date.year
        month = f"{sale_date.month:02d}"
        day = f"{sale_date.day:02d}"

        path = base / f"year={year}" / f"month={month}" / f"day={day}"
        path.mkdir(parents=True, exist_ok=True)

     
        final_name = f"part-{source_file_id}.parquet"
        tmp_name = f".{final_name}.tmp"

        table = pa.Table.from_pandas(
            group,
            preserve_index=False
        )

        tmp_path = path / tmp_name
        final_path = path / final_name

        pq.write_table(table, tmp_path, compression="snappy")
        tmp_path.replace(final_path)



def write_partitions_s3(df, *, source_file_id: str, shop_id: str):
    for sale_date, group in df.groupby("sale_date"):
        year = sale_date.year
        month = f"{sale_date.month:02d}"
        day = f"{sale_date.day:02d}"

        filename = {
            f"{shop_id}_"
            f"{sale_date:%Y%m%d}_"
            f"{source_file_id}.parquet"
        }


        key = (
            f"curated/sales/"
            f"year={year}/month={month}/day={day}/"
            f"part-{source_file_id}.parquet"
        )

        table = pa.Table.from_pandas(group, preserve_index=False)
        buffer = BytesIO()
        pq.write_table(table, buffer, compression="snappy")

        s3.put_object(
            Bucket=CURATED_BUCKET,
            Key=key,
            Body=buffer.getvalue(),
        )