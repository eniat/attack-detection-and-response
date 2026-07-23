from types import SimpleNamespace
from datetime import datetime, timedelta

from app.services.detection_engine import detect_brute_force

def failed_signin(offset_minutes):
    return SimpleNamespace(
        event_type="signin",
        status="failure",
        ip_address="203.0.113.45",
        user_principal_name="user25@contoso.com",
        timestamp=datetime(2026, 6, 1, 9, 0, 0) + timedelta(minutes= offset_minutes)
    )

def test_detects_brute_force_within_window():

    events = [failed_signin(index) for index in range(12)]
    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-002"
    assert alerts[0]["mitre_technique_id"] == "T1110"

def test_does_not_alert_when_failures_are_spread_over_months():
    
    events = [failed_signin(index * 60 * 24 * 7) for index in range(12)]
    alerts = detect_brute_force(events)

    assert alerts == []