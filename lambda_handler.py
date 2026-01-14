def lambda_handler(event, context):
    # Orchestrate:
    # 1) list raw files (lookback)
    # 2) load bytes + metadata (sender, file_id)
    # 3) read → transform → write by sale_date
    return {"status": "ok"}
