from types import SimpleNamespace

from app.services.detection_engine import detect_suspicious_mailbox_rule

def test_detects_suspicious_mailbox_rule():
    events = [
        SimpleNamespace(
            operation= "New-InboxRule",
            user_principal_name= "user29@contoso.com",
            ip_address="203.0.113.88",
            details= '{"forward_to": "external.receiver@example.net"}'
        )
    ]


    alerts = detect_suspicious_mailbox_rule(events)

    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "DET-006"
    assert alerts[0]["mitre_technique_id"] == "T1114"