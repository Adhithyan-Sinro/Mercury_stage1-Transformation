# import boto3
# import pyarrow as pa
# import pyarrow.parquet as pq
# import pandas as pd
# from app.config import CURATED_BUCKET, AWS_REGION

# s3 = boto3.client("s3", region_name=AWS_REGION)

# def write_parquet(df, *, sale_date):
#     year = sale_date.year
#     month = f"{sale_date.month:02d}"
#     day = f"{sale_date.day:02d}"

#     key_prefix = f"curated/sales/year={year}/month={month}/day={day}/"
#     table = pa.Table.from_pandas(df)
#     buffer = pa.BufferOutputStream()
#     pq.write_table(table, buffer, compression="snappy")

#     s3.put_object(
#         Bucket=CURATED_BUCKET,
#         Key=f"{key_prefix}part-{int(pd.Timestamp.utcnow().timestamp())}.parquet",
#         Body=buffer.getvalue().to_pybytes()
#     )



import os
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow as pa

def write_partitions(df):
    for sale_date, group in df.groupby("sale_date"):
        year = sale_date.year
        month = f"{sale_date.month:02d}"
        day = f"{sale_date.day:02d}"

        base = Path("local_curated_output")
        path = base / f"year={year}" / f"month={month}" / f"day={day}"
        path.mkdir(parents=True, exist_ok=True)

        table = pa.Table.from_pandas(group)
        pq.write_table(
            table,
            path / "part-local.parquet",
            compression="snappy"
        )

