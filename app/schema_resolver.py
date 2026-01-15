import pandas as pd
from app.shop_schema_config import SHOP_SCHEMAS


class SchemaResolutionError(ValueError):
    pass


def resolve_schema(df: pd.DataFrame, *, shop_id: str) -> pd.DataFrame:
    if shop_id not in SHOP_SCHEMAS:
        raise SchemaResolutionError(f"NO_SCHEMA_DEFINED_FOR_SHOP: {shop_id}")

    schema = SHOP_SCHEMAS[shop_id]
    cols = schema.get("columns", {})

    if not cols:
        raise SchemaResolutionError(f"EMPTY_SCHEMA: shop={shop_id}")

    

    # Enforce consistent mapping strategy
    strategies = {tuple(spec.keys())[0] for spec in cols.values()}
    if len(strategies) != 1:
        raise SchemaResolutionError(
            f"MIXED_SCHEMA_MAPPING_STRATEGY: shop={shop_id}"
        )
    
    if "index" in strategies:
        max_idx = max(spec["index"] for spec in cols.values())
        if df.shape[1] <= max_idx:
            raise SchemaResolutionError(
                f"INSUFFICIENT_COLUMNS: shop={shop_id}, "
                f"expected_at_least={max_idx+1}, got={df.shape[1]}"
            )
        
    out = pd.DataFrame(index=df.index)

    for target_col, spec in cols.items():
        if "index" in spec:
            out[target_col] = df.iloc[:, spec["index"]]
        elif "name" in spec:
            if spec["name"] not in df.columns:
                raise SchemaResolutionError(
                    f"COLUMN_NAME_NOT_FOUND: shop={shop_id}, "
                    f"target={target_col}, name={spec['name']}"
                )
            # idx = spec["index"]
            # if idx >= df.shape[1]:
            #     raise SchemaResolutionError(
            #         f"COLUMN_INDEX_OUT_OF_RANGE: shop={shop_id}, "
            #         f"target={target_col}, index={idx}, max_index={df.shape[1]-1}"
            #     )
            # out[target_col] = df.iloc[:, idx]

            out[target_col] = df[spec["name"]]
        
        if target_col == "amount":
            out[target_col] = pd.to_numeric(
                out[target_col], errors="coerce"
            )

        # elif "name" in spec:
        #     name = spec["name"]
        #     if name not in df.columns:
        #         raise SchemaResolutionError(
        #             f"COLUMN_NAME_NOT_FOUND: shop={shop_id}, "
        #             f"target={target_col}, name={name}"
        #         )
        #     out[target_col] = df[name]

        # else:
        #     raise SchemaResolutionError(
        #         f"INVALID_SCHEMA_SPEC: shop={shop_id}, target={target_col}"
        #     )

    return out
