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

def test_does_not_alert_for_internal_forwarding():

    events = [
        SimpleNamespace(
            operation="New-InboxRule",
            user_principal_name="user29@contoso.com",
            ip_address="203.0.113.88",
            details='{"forward_to": "helpdesk@contoso.com"}'
        )
    ]
    assert detect_suspicious_mailbox_rule(events) == []

def test_does_not_alert_for_rules_without_a_forwarding_address():

    events = [
        SimpleNamespace(
            operation="New-InboxRule",
            user_principal_name="user29@contoso.com",
            ip_address="203.0.113.88",
            details='{"rule_name": "Move newsletters", "move_to_folder": "Archive"}'
        )
    ]
    assert detect_suspicious_mailbox_rule(events) == []