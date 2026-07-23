import json
from collections import defaultdict, Counter
from datetime import timedelta

from app.config import settings

# Detection tuning mirroed documented thresholds in /detections/*.yml
PASSWORD_SPRAY_WINDOW = timedelta(minutes= 60)
PASSWORD_SPRAY_MIN_FAILURES = 20
PASSWORD_SPRAY_MIN_USERS = 10

BRUTE_FORCE_WINDOW = timedelta(minutes= 30)
BRUTE_FORCE_MIN_FAILURES = 10

MFA_FATIGUE_WINDOW = timedelta(minutes= 60)
MFA_FATIGUE_MIN_DENIALS = 5

MAILBOX_FORWARD_KEYS = ("forward_to", "redirect_to","forward_as_attachment_to")

def has_timestamp(event):
    """
        Guards against rows where pandas coerced unparseable timestamp
    """

    timestamp = getattr(event,"timestamp", None)
    return timestamp is not None and timestamp == timestamp


def find_densest_window(sorted_events, window_length, is_match):
    """
        Given a list of events sorted by timestamp, find the densest window of time
    """

    best_window = None
    user_counts = Counter()
    left = 0

    for right, event in enumerate(sorted_events):
        user_counts[event.user_principal_name] += 1

        while sorted_events[right].timestamp - sorted_events[left].timestamp > window_length:
            dropped = sorted_events[left].user_principal_name
            user_counts[dropped] -= 1
            if user_counts[dropped] == 0:
                del user_counts[dropped]
            left += 1

        current = sorted_events[left:right + 1]

        if is_match(current, user_counts) and (best_window is None or len(current) > len(best_window)):
            best_window = current

    return best_window


def find_mfa_fatigue_approval(user_events):
    """
        Return the first MFA approval preceded by enough recent denials and those denials
    """

    sorted_events = sorted(user_events, key=lambda event: event.timestamp)

    for index, event in enumerate(sorted_events):
        if event.mfa_result != "success":
            continue

        preceding_denials =[
            candidate for candidate in sorted_events[:index]
            if candidate.mfa_result == "denied"
            and event.timestamp - candidate.timestamp <= MFA_FATIGUE_WINDOW
        ]

        if len(preceding_denials) >= MFA_FATIGUE_MIN_DENIALS:
            return event, preceding_denials

    return None, []


def extract_forwarding_address(details):
    """
        Pull a forwarding address out of the audit details JSON
    """

    if not details:
        return None

    try:
        parsed = json.loads(details)
    except (TypeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None

    for key in MAILBOX_FORWARD_KEYS:
        value = parsed.get(key)

        if isinstance(value, str) and "@" in value:
            return value.strip()

        if isinstance(value, list) and value:
            first = str(value[0]).strip()
            if "@" in first:
                return first
    return None


def is_external_address(address):
    """
        True when the address domain is not one of the internal domains
    """

    domain = address.split("@")[-1].strip().lower()

    if not domain:
        return False

    return not any(
        domain == internal or domain.endswith("." + internal)
        for internal in settings.INTERNAL_DOMAINS
    )


def run_all_detections(events):

    alerts = []
    alerts.extend(detect_password_spray(events))
    alerts.extend(detect_brute_force(events))
    alerts.extend(detect_impossible_travel(events))
    alerts.extend(detect_mfa_fatigue(events))
    alerts.extend(detect_suspicious_oauth_consent(events))
    alerts.extend(detect_suspicious_mailbox_rule(events))

    return alerts

def detect_password_spray(events):

    alerts = []
    failures_by_ip = defaultdict(list)

    for event in events:
        if event.event_type == "signin" and event.status == "failure" and has_timestamp(event):
            failures_by_ip[event.ip_address].append(event)

    for ip_address, failed_events in failures_by_ip.items():
        window = find_densest_window(
            sorted(failed_events, key=lambda event: event.timestamp),
            PASSWORD_SPRAY_WINDOW,
            lambda slice_events, user_counts: (
                len(slice_events) >= PASSWORD_SPRAY_MIN_FAILURES
                and len(user_counts) >= PASSWORD_SPRAY_MIN_USERS
            )
        )

        if window:
            unique_users = {event.user_principal_name for event in window}

            evidence = {
                "source_ip": ip_address,
                "failed_login_count": len(window),
                "unique_users_targeted": len(unique_users),
                "sample_targeted_users": sorted(unique_users)[:10],
                "window_minutes": int(PASSWORD_SPRAY_WINDOW.total_seconds() // 60),
                "first_seen": str(window[0].timestamp),
                "last_seen": str(window[-1].timestamp)
            }

            alerts.append({
                "rule_id": "DET-001",
                "rule_name": "Password Spray Attack",
                "title": f"Password spray detected from {ip_address}",
                "description": "One source IP generated failed login attempts against many different users within a short window.",
                "severity": "High",
                "score": 80,
                "affected_user": "multiple",
                "source_ip": ip_address,
                "mitre_technique_id": "T1110.003",
                "mitre_technique_name": "Password Spraying",
                "evidence": json.dumps(evidence)
            })

    return alerts

def detect_brute_force(events):
    alerts = []
    failures_by_ip_and_user = defaultdict(list)

    for event in events:
        if event.event_type == "signin" and event.status == "failure" and has_timestamp(event):
            key = (event.ip_address, event.user_principal_name)
            failures_by_ip_and_user[key].append(event)

    for (ip_address, user),failed_events in failures_by_ip_and_user.items():
        window = find_densest_window(
            sorted(failed_events, key=lambda event: event.timestamp),
            BRUTE_FORCE_WINDOW,
            lambda slice_events, user_counts: len(slice_events) >= BRUTE_FORCE_MIN_FAILURES
        )

        if window:
            evidence = {
                "source_ip": ip_address,
                "target_user": user,
                "failed_login_count": len(window),
                "window_minutes": int(BRUTE_FORCE_WINDOW.total_seconds() // 60),
                "first_seen": str(window[0].timestamp),
                "last_seen": str(window[-1].timestamp)
            }

            alerts.append({
                "rule_id": "DET-002",
                "rule_name": "Brute Force Login Attempt",
                "title": f"Brute force attempt against {user}",
                "description":"One source IP repeatedly failed authentication against one user within a short window.",
                "severity": "Medium",
                "score": 60,
                "affected_user": user,
                "source_ip": ip_address,
                "mitre_technique_id": "T1110",
                "mitre_technique_name": "Brute Force",
                "evidence": json.dumps(evidence)
            })

    return alerts

def detect_impossible_travel(events):

    alerts = []
    successful_logins_by_user = defaultdict(list)

    for event in events:
        if event.event_type == "signin" and event.status =="success":
            successful_logins_by_user[event.user_principal_name].append(event)

    for user, user_events in successful_logins_by_user.items():
        sorted_events = sorted(user_events, key=lambda event: event.timestamp)

        for index in range(len(sorted_events) - 1):
            first_event = sorted_events[index]
            second_event = sorted_events[index + 1]

            different_country = first_event.country != second_event.country
            time_difference = second_event.timestamp - first_event.timestamp

            if different_country and time_difference <= timedelta(hours=2):
                evidence = {
                    "user": user,
                    "first_country":first_event.country,
                    "second_country": second_event.country,
                    "first_time": str(first_event.timestamp),
                    "second_time": str(second_event.timestamp)
                }

                alerts.append({
                    "rule_id": "DET-003",
                    "rule_name": "Impossible Travel",
                    "title": f"Impossible travel detected for {user}",
                    "description": "The same user successfully authenticated from different countries within an unrealistic time window.",
                    "severity":"High",
                    "score": 75,
                    "affected_user": user,
                    "source_ip": second_event.ip_address,
                    "mitre_technique_id": "T1078",
                    "mitre_technique_name": "Valid Accounts",
                    "evidence": json.dumps(evidence)
                })

    return alerts

def detect_mfa_fatigue(events):

    alerts = []
    events_by_user = defaultdict(list)

    for event in events:
        if event.event_type == "signin" and has_timestamp(event):
            events_by_user[event.user_principal_name].append(event)

    for user, user_events in events_by_user.items():
        approval, preceding_denials = find_mfa_fatigue_approval(user_events)

        if approval:
            evidence = {
                "user": user,
                "mfa_denied_count": len(preceding_denials),
                "first_denial": str(preceding_denials[0].timestamp),
                "last_denial": str(preceding_denials[-1].timestamp),
                "approval_time": str(approval.timestamp),
                "approval_ip": approval.ip_address,
                "window_minutes": int(MFA_FATIGUE_WINDOW.total_seconds() // 60)
            }

            alerts.append({
                "rule_id": "DET-004",
                "rule_name": "MFA Fatigue",
                "title": f"MFA fatigue pattern detected for {user}",
                "description": "Multiple MFA denials were followed by a successful MFA approval within a short window.",
                "severity": "High",
                "score": 85,
                "affected_user": user,
                "source_ip": approval.ip_address,
                "mitre_technique_id": "T1621",
                "mitre_technique_name":"Multi-Factor Authentication Request Generation",
                "evidence": json.dumps(evidence)
            })

    return alerts

def detect_suspicious_oauth_consent(events):

    alerts = []
    suspicious_permissions = [
        "Mail.Read",
        "Files.Read.All",
        "offline_access"]

    for event in events:
        if event.operation == "ConsentToApplication":
            details = event.details or ""

            if any(permission in details for permission in suspicious_permissions):
                evidence = {
                    "user": event.user_principal_name,
                    "operation": event.operation,
                    "details": details
                }

                alerts.append({
                    "rule_id": "DET-005",
                    "rule_name": "Suspicious OAuth Consent",
                    "title": f"Suspicious OAuth consent by {event.user_principal_name}",
                    "description": "User granted potentially risky OAuth permissions to an application.",
                    "severity": "High",
                    "score": 80,
                    "affected_user": event.user_principal_name,
                    "source_ip": event.ip_address,
                    "mitre_technique_id": "T1566",
                    "mitre_technique_name": "Phishing",
                    "evidence":json.dumps(evidence)
                })

    return alerts

def detect_suspicious_mailbox_rule(events):
    alerts = []

    for event in events:
        forwarding_address = extract_forwarding_address(event.details)

        if (event.operation == "New-InboxRule" and forwarding_address
                and is_external_address(forwarding_address)):

            evidence = {
                "user": event.user_principal_name,
                "operation": event.operation,
                "forward_to": forwarding_address,
                "forward_to_domain": forwarding_address.split("@")[-1].lower(),
                "internal_domains": sorted(settings.INTERNAL_DOMAINS),
                "details": event.details
            }

            alerts.append({
                "rule_id": "DET-006",
                "rule_name": "Suspicious Mailbox Forwarding Rule",
                "title": f"External mailbox forwarding rule created by {event.user_principal_name}",
                "description": "A mailbox rule was created to forward messages to an address outside the internal domains.",
                "severity": "Critical",
                "score": 90,
                "affected_user": event.user_principal_name,
                "source_ip": event.ip_address,
                "mitre_technique_id": "T1114",
                "mitre_technique_name": "Email Collection",
                "evidence":json.dumps(evidence)
            })

    return alerts