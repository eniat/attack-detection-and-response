from types import SimpleNamespace

from app.services.detection_engine import detect_brute_force

def test_detects_brute_force():
    events = []

    for index in range(12):
        events.append(SimpleNamespace(
            event_type= "signin",
            status= "failure",
            ip_address="203.0.113.45",
            user_principal_name= "user25@contoso.com"
        ))

    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-002"
    assert alerts[0]["mitre_technique_id"] == "T1110"