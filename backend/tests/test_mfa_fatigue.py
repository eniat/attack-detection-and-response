from types import SimpleNamespace
from datetime import datetime, timedelta

from app.services.detection_engine import detect_mfa_fatigue

USER = "user27@contoso.com"

def signin(mfa_result, offset_minutes):
    return SimpleNamespace(
        event_type="signin",
        user_principal_name=USER,
        ip_address="198.51.100.77",
        mfa_result=mfa_result,
        timestamp=datetime(2026, 6, 1, 9, 0, 0) + timedelta(minutes= offset_minutes)
    )

def test_detects_denials_followed_by_approval():

    events = [signin("denied", index) for index in range(5)]
    events.append(signin("success", 6))
    alerts = detect_mfa_fatigue(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-004"
    assert alerts[0]["mitre_technique_id"] == "T1621"

def test_does_not_alert_when_approval_precedes_denials():

    events = [signin("success", 0)]
    events.extend(signin("denied", 60 + index) for index in range(5))
    alerts = detect_mfa_fatigue(events)

    assert alerts == []

def test_does_not_alert_when_denials_are_outside_the_window():

    events = [signin("denied", index) for index in range(5)]
    events.append(signin("success", 600))
    alerts = detect_mfa_fatigue(events)

    assert alerts == []