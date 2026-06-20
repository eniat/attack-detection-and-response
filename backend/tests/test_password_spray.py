from datetime import datetime
from types import SimpleNamespace

from app.services.detection_engine import detect_password_spray

def test_detects_password_spray():
    
    events = []

    for index in range(25):
        events.append(SimpleNamespace(
            event_type= "signin",
            status="failure",
            ip_address="185.22.10.4",
            user_principal_name=f"user{index}@contoso.com",
            timestamp=datetime(2026, 6, 1, 9, 0, index)
        ))

    alerts = detect_password_spray(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-001"
    assert alerts[0]["severity"] == "High"
    assert alerts[0]["mitre_technique_id"] == "T1110.003"


def test_does_not_alert_for_single_user_failures():
    events = []

    for index in range(25):
        events.append(SimpleNamespace(
            event_type= "signin",
            status="failure",
            ip_address="185.22.10.4",
            user_principal_name="sameuser@contoso.com",
            timestamp=datetime(2026, 6, 1, 9, 0, index)
        ))

    alerts = detect_password_spray(events)

    assert len(alerts) == 0