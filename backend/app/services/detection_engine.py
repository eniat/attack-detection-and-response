import json
from collections import defaultdict

def run_all_detections(events):

    alerts = []
    alerts.extend(detect_password_spray(events))

    return alerts

def detect_password_spray(events):

    alerts = []
    failures_by_ip = defaultdict(list)

    for event in events:
        if event.event_type == "signin" and event.status == "failure":
            failures_by_ip[event.ip_address].append(event)

    for ip_address, failed_events in failures_by_ip.items():
        unique_users = {event.user_principal_name for event in failed_events}
        failed_count = len(failed_events)

        if failed_count >= 20 and len(unique_users) >= 10:
            sorted_events = sorted(failed_events, key=lambda event: event.timestamp)

            evidence = {
                "source_ip": ip_address,
                "failed_login_count": failed_count,
                "unique_users_targeted": len(unique_users),
                "sample_targeted_users": list(unique_users)[:10],
                "first_seen": str(sorted_events[0].timestamp),
                "last_seen": str(sorted_events[-1].timestamp)
            }

            alerts.append({
                "rule_id": "DET-001",
                "rule_name": "Password Spray Attack",
                "title": f"Password spray detected from {ip_address}",
                "description": "One source IP generated failed login attempts against many different users.",
                "severity": "High",
                "score": 80,
                "affected_user": "multiple",
                "source_ip": ip_address,
                "mitre_technique_id": "T1110.003",
                "mitre_technique_name": "Password Spraying",
                "evidence": json.dumps(evidence)
            })

    return alerts