import pandas as pd


REQUIRED_COLUMNS = [
    "event_id",
    "timestamp",
    "user_principal_name",
    "event_type",
    "ip_address",
    "country",
    "city",
    "user_agent",
    "application",
    "status",
    "failure_reason",
    "mfa_result",
    "client_app",
    "operation",
    "target_resource",
    "details"
]


def parse_csv_upload(file_obj):
    df =pd.read_csv(file_obj)

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["timestamp"] = pd.to_datetime( df["timestamp"], errors="coerce")

    events = []

    for _ , row in df.iterrows():
        events.append({
            "event_id": clean_value(row.get("event_id")),
            "timestamp": row.get("timestamp"),
            "user_principal_name": clean_value(row.get("user_principal_name")),
            "event_type": clean_value(row.get("event_type")),
            "ip_address": clean_value(row.get("ip_address")),
            "country": clean_value(row.get("country")),
            "city": clean_value(row.get("city")),
            "user_agent": clean_value(row.get("user_agent")),
            "application" : clean_value(row.get("application")),
            "status": clean_value(row.get("status")),
            "failure_reason": clean_value(row.get("failure_reason")),
            "mfa_result": clean_value(row.get("mfa_result")),
            "client_app": clean_value(row.get("client_app")),
            "operation": clean_value(row.get("operation")),
            "target_resource": clean_value(row.get("target_resource")),
            "details": clean_value(row.get("details"))
        })

    return events


def clean_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()