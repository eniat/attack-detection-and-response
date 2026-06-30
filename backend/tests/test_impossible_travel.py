from datetime import datetime, timedelta
from types import SimpleNamespace

from app.services.detection_engine import detect_impossible_travel


def test_detects_impossible_travel():
    user = "user26@contoso.com"

    events = [
        SimpleNamespace(
            event_type= "signin",
            status= "success",
            ip_address="51.140.80.12",
            user_principal_name= user,
            country= "United Kingdom",
            timestamp=datetime(2026, 6, 1, 9, 0, 0)
        ),
        SimpleNamespace(
            event_type= "signin",
            status= "success",
            ip_address="13.236.90.22",
            user_principal_name= user,
            country= "Australia",
            timestamp=datetime(2026, 6, 1, 10, 35, 0)
        )
    ]

    alerts = detect_impossible_travel(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-003"
    assert alerts[0]["mitre_technique_id"] == "T1078"