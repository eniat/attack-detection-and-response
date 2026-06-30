from types import SimpleNamespace

from app.services.detection_engine import detect_mfa_fatigue

def test_detects_mfa_fatigue():
    events = []
    user = "user27@contoso.com"

    for index in range(5):
        events.append(SimpleNamespace(
            event_type= "signin",
            user_principal_name= user,
            ip_address="198.51.100.77",
            mfa_result= "denied"
        ))

    events.append(SimpleNamespace(
        event_type= "signin",
        user_principal_name= user,
        ip_address="198.51.100.77",
        mfa_result= "success"
    ))

    alerts = detect_mfa_fatigue(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-004"
    assert alerts[0]["mitre_technique_id"] == "T1621"