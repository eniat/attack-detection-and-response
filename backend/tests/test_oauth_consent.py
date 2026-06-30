from types import SimpleNamespace

from app.services.detection_engine import detect_suspicious_oauth_consent


def test_detects_suspicious_oauth_consent():
    events = [
        SimpleNamespace(
            operation= "ConsentToApplication",
            user_principal_name= "user28@contoso.com",
            ip_address="192.0.2.88",
            details= '{"permissions": ["Mail.Read", "offline_access"]}'
        )
    ]

    alerts = detect_suspicious_oauth_consent(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-005"
    assert alerts[0]["mitre_technique_id"] == "T1566"