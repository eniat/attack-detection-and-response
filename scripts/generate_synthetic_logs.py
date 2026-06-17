import csv
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path("sample_logs")
OUTPUT_FILE = OUTPUT_DIR / "password_spray_attack.csv"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    start_time = datetime(2026, 6, 1, 9, 0, 0)

    rows = []

    for i in range(25):
        rows.append({
            "event_id": f"evt-{i:03}",
            "timestamp": (start_time + timedelta(seconds=i * 20)).isoformat(),
            "user_principal_name": f"user{i}@contoso.com",
            "event_type": "signin",
            "ip_address": "185.22.10.4",
            "country": "Russia",
            "city": "Moscow",
            "user_agent": "Mozilla/5.0 Chrome",
            "application": "Microsoft 365",
            "status": "failure",
            "failure_reason": "Invalid password",
            "mfa_result": "not_required",
            "client_app": "browser",
            "operation": "UserLoginFailed",
            "target_resource": "Microsoft 365",
            "details": "{}",
        })

    rows.append({
        "event_id": "evt-999",
        "timestamp": (start_time + timedelta(minutes=12)).isoformat(),
        "user_principal_name": "user7@contoso.com",
        "event_type": "signin",
        "ip_address": "185.22.10.4",
        "country": "Russia",
        "city": "Moscow",
        "user_agent": "Mozilla/5.0 Chrome",
        "application": "Microsoft 365",
        "status": "success",
        "failure_reason": "",
        "mfa_result": "success",
        "client_app": "browser",
        "operation": "UserLoggedIn",
        "target_resource": "Microsoft 365",
        "details": "{}",
    })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()