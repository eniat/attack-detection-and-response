import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path("sample_logs")

FIELDNAMES = [
    "event_id",
    "timestamp",
    "user_principal_name",
    "event_type",
    "ip_address",
    "country",
    "city",
    "user_agent",
    "application",
    "status",
    "failure_reason",
    "mfa_result",
    "client_app",
    "operation",
    "target_resource",
    "details"
]

SCENARIO_FILES = {
    "password_spray": "password_spray_attack.csv",
    "brute_force": "brute_force_attack.csv",
    "impossible_travel": "impossible_travel.csv",
    "mfa_fatigue": "mfa_fatigue.csv",
    "oauth_consent_abuse": "oauth_consent_abuse.csv",
    "mailbox_forwarding_abuse": "mailbox_forwarding_abuse.csv",
    "combined_identity_compromise": "combined_identity_compromise.csv"
}

DEFAULT_ROW = {
    "event_type": "audit",
    "ip_address": "192.0.2.10",
    "country": "United Kingdom",
    "city": "London",
    "user_agent": "Mozilla/5.0 Chrome",
    "application": "Microsoft 365",
    "status": "success",
    "failure_reason": "",
    "mfa_result": "not_required",
    "client_app": "browser",
    "target_resource": "Microsoft 365"
}

SIGNIN = {"event_type": "signin"}
ACCESS = {"event_type": "access"}
AAD_AUDIT = {"event_type": "audit", "application": "Azure Active Directory"}
EXCHANGE_PS = {
    "event_type": "audit",
    "user_agent": "ExchangePowerShell/1.0",
    "application": "Exchange Online",
    "client_app": "powershell"
}

def minutes(value):
    return timedelta(minutes=value)

def seconds(value):
    return timedelta(seconds=value)

def details(**values):
    return json.dumps(values, sort_keys=True)

def make_row(event_id, timestamp, user, operation, detail=None, **overrides):
    row = {
        **DEFAULT_ROW,
        **overrides,
        "event_id": event_id,
        "timestamp": timestamp.isoformat(),
        "user_principal_name": user,
        "operation": operation,
        "details": details(**detail) if detail else "{}"
    }

    return {field: row[field] for field in FIELDNAMES}

def add_event(rows, prefix, index, start_time, offset, user, operation, scenario=None, detail=None, **overrides):
    detail_required = operation in ["ConsentToApplication", "New-InboxRule"]

    rows.append(make_row(
        event_id=f"evt-{len(rows):03}",
        timestamp=start_time + offset,
        user=user,
        operation=operation,
        detail=detail if detail_required else None,
        **overrides
    ))


def add_sequence(rows, prefix, start_time, user, scenario, shared, steps, start_index=0):
    for index, step in enumerate(steps, start=start_index):
        offset, operation, detail, overrides = step

        add_event(
            rows,
            prefix,
            index,
            start_time,
            offset,
            user,
            operation,
            scenario,
            detail,
            **{**shared, **overrides}
        )

def write_csv(filename, rows):
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / filename

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {output_file} ({len(rows)} rows)")

def build_password_spray(start_time, event_prefix="ps", scenario="password_spray"):
    rows = []
    source_ip = "185.22.10.4"
    source = {"ip_address": source_ip, "country": "Russia", "city": "Moscow"}

    for i in range(25):
        add_event(
            rows,
            event_prefix,
            i,
            start_time,
            seconds(i * 20),
            f"user{i + 1}@contoso.com",
            "UserLoginFailed",
            scenario,
            {"source_ip": source_ip, "attempt": i + 1},
            **SIGNIN,
            **source,
            status="failure",
            failure_reason="Invalid password",
            mfa_result="not_required"
        )

    return rows

def build_brute_force(start_time, event_prefix="bf"):
    rows = []
    user = "user25@contoso.com"
    source_ip = "203.0.113.45"
    source = {
        "ip_address": source_ip,
        "country": "United States",
        "city": "New York",
        "user_agent": "Mozilla/5.0 Firefox"
    }

    for i in range(15):
        add_event(
            rows,
            event_prefix,
            i,
            start_time,
            seconds(i * 15),
            user,
            "UserLoginFailed",
            "brute_force",
            {"attempt": i + 1, "source_ip": source_ip},
            **SIGNIN,
            **source,
            status="failure",
            failure_reason="Invalid password",
            mfa_result="not_required"
        )

    add_event(
        rows,
        event_prefix,
        15,
        start_time,
        minutes(5),
        user,
        "UserLoggedIn",
        "brute_force",
        {"result": "successful_login_after_failures"},
        **SIGNIN,
        **source,
        mfa_result="success"
    )

    return rows

def build_impossible_travel(start_time, event_prefix="it"):
    rows = []
    user = "user26@contoso.com"
    uk = {"ip_address": "51.140.80.12", "country": "United Kingdom", "city": "London"}
    au = {"ip_address": "13.236.90.22", "country": "Australia", "city": "Sydney"}

    steps = [
        (minutes(0), "UserLoggedIn", {"sequence": "uk_success"}, {**SIGNIN, **uk, "mfa_result": "success"}),
        (minutes(3), "MailboxAccessed", {"sequence": "uk_mailbox_access"}, {**ACCESS, **uk, "application": "Outlook", "target_resource": "Exchange Online"}),
        (minutes(7), "FileAccessed", {"sequence": "uk_sharepoint_access"}, {**ACCESS, **uk, "application": "SharePoint Online", "target_resource": "SharePoint Online"}),
        (minutes(95), "UserLoggedIn", {"sequence": "australia_success", "hours_since_previous": 1.58}, {**SIGNIN, **au, "mfa_result": "success"}),
        (minutes(98), "MailboxAccessed", {"sequence": "australia_mailbox_access"}, {**ACCESS, **au, "application": "Outlook", "target_resource": "Exchange Online"}),
        (minutes(102), "TeamsSessionStarted", {"sequence": "australia_teams_access"}, {**ACCESS, **au, "application": "Teams", "target_resource": "Microsoft Teams"})
    ]

    add_sequence(rows, event_prefix, start_time, user, "impossible_travel", {}, steps)
    return rows


def build_mfa_fatigue(start_time, event_prefix="mfa"):
    rows = []
    user = "user27@contoso.com"
    source = {"ip_address": "198.51.100.77", "country": "Netherlands", "city": "Amsterdam"}

    add_event(
        rows,
        event_prefix,
        0,
        start_time,
        minutes(0),
        user,
        "UserLoginMfaRequired",
        "mfa_fatigue",
        {"stage": "initial_login_attempt"},
        **SIGNIN,
        **source,
        status="failure",
        failure_reason="MFA required",
        mfa_result="challenge_required"
    )

    for i in range(5):
        add_event(
            rows,
            event_prefix,
            i + 1,
            start_time,
            seconds((i + 1) * 30),
            user,
            "MfaDenied",
            "mfa_fatigue",
            {"prompt_number": i + 1},
            **SIGNIN,
            **source,
            status="failure",
            failure_reason="MFA denied by user",
            mfa_result="denied"
        )

    add_event(
        rows,
        event_prefix,
        6,
        start_time,
        minutes(3),
        user,
        "MfaSatisfied",
        "mfa_fatigue",
        {"result": "accepted_after_repeated_denials"},
        **SIGNIN,
        **source,
        mfa_result="success"
    )

    add_event(
        rows,
        event_prefix,
        7,
        start_time,
        minutes(4),
        user,
        "MailboxAccessed",
        "mfa_fatigue",
        {"stage": "mailbox_access_after_mfa_success"},
        **ACCESS,
        **source,
        application="Outlook",
        target_resource="Exchange Online"
    )

    return rows

def build_oauth_consent_abuse(start_time, event_prefix="oauth"):
    rows = []
    user = "user28@contoso.com"
    app_id = "8f12b88a-4f0d-470c-9e60-2e9819b34f91"
    app_name = "Finance Report Exporter"

    shared = {"ip_address": "192.0.2.88", "country": "Germany", "city": "Frankfurt"}
    aad = {**AAD_AUDIT, "target_resource": app_name}

    steps = [
        (minutes(0), "UserLoggedIn", {"stage": "user_login"}, {**SIGNIN, "application": "Microsoft 365", "target_resource": "Microsoft 365", "mfa_result": "success"}),
        (minutes(2), "ApplicationRegistered", {"app_id": app_id, "app_name": app_name}, aad),
        (minutes(3), "ServicePrincipalCreated", {"app_id": app_id, "app_name": app_name}, aad),
        (minutes(4), "ConsentToApplication", {"app_id": app_id, "app_name": app_name, "permissions": ["Mail.Read", "offline_access"]}, aad),
        (minutes(6), "TokenIssued", {"app_id": app_id, "app_name": app_name, "scope": "Mail.Read offline_access"}, aad)
    ]

    add_sequence(rows, event_prefix, start_time, user, "oauth_consent_abuse", shared, steps)
    return rows


def build_mailbox_forwarding_abuse(start_time, event_prefix="mbx"):
    rows = []
    user = "user29@contoso.com"
    forward_to = "external.receiver@example.net"
    shared = {"ip_address": "203.0.113.88", "country": "United Kingdom", "city": "Manchester"}
    exchange = {**EXCHANGE_PS, "target_resource": "Exchange Online Mailbox"}

    steps = [
        (minutes(0), "UserLoggedIn", {"stage": "user_login"}, {**SIGNIN, "mfa_result": "success"}),
        (minutes(2), "ExchangePowerShellSessionStarted", {"stage": "exchange_powershell_connected"}, {**EXCHANGE_PS, "target_resource": "Exchange Online"}),
        (minutes(4), "New-InboxRule", {"rule_name": "Auto forward invoices", "forward_to": forward_to, "delete_message": False}, exchange),
        (minutes(6), "Set-Mailbox", {"forwarding_smtp_address": forward_to, "deliver_to_mailbox_and_forward": True}, exchange),
        (minutes(8), "MailboxAccessed", {"stage": "mailbox_access_after_rule_creation"}, {**ACCESS, "application": "Outlook", "target_resource": "Exchange Online"})
    ]

    add_sequence(rows, event_prefix, start_time, user, "mailbox_forwarding_abuse", shared, steps)
    return rows


def build_combined_identity_compromise(start_time):
    rows = []
    user = "user7@contoso.com"
    app_id = "a2f21d3e-7c34-4d91-a5d1-fbb44a2cf2ef"
    app_name = "Document Sync Helper"
    forward_to = "attacker.dropbox@example.net"

    rows.extend(build_password_spray(start_time, "combined-ps", "combined_identity_compromise"))

    shared = {"ip_address": "185.22.10.4", "country": "Russia", "city": "Moscow"}
    exchange = {**EXCHANGE_PS, "target_resource": "Exchange Online Mailbox"}
    aad = {**AAD_AUDIT, "target_resource": app_name}

    steps = [
        (minutes(12), "UserLoggedIn", {"stage": "successful_login_after_spray"}, {**SIGNIN, "mfa_result": "success"}),
        (minutes(14), "MailboxAccessed", {"stage": "mailbox_access"}, {**ACCESS, "application": "Outlook", "target_resource": "Exchange Online"}),
        (minutes(16), "FileAccessed", {"stage": "sharepoint_access"}, {**ACCESS, "application": "SharePoint Online", "target_resource": "SharePoint Online"}),
        (minutes(18), "ExchangePowerShellSessionStarted", {"stage": "exchange_powershell_connected"}, {**EXCHANGE_PS, "target_resource": "Exchange Online"}),
        (minutes(20), "New-InboxRule", {"stage": "mailbox_forwarding", "rule_name": "Invoice processing", "forward_to": forward_to}, exchange),
        (minutes(22), "Set-Mailbox", {"stage": "mailbox_forwarding", "forwarding_smtp_address": forward_to, "deliver_to_mailbox_and_forward": True}, exchange),
        (minutes(24), "ApplicationRegistered", {"stage": "oauth_application_registered", "app_id": app_id, "app_name": app_name}, aad),
        (minutes(26), "ConsentToApplication", {"stage": "oauth_consent", "app_id": app_id, "app_name": app_name, "permissions": ["Mail.Read", "offline_access"]}, aad),
        (minutes(28), "TokenIssued", {"stage": "token_issued", "app_id": app_id, "scope": "Mail.Read offline_access"}, aad)
    ]

    add_sequence(rows, "combined", start_time, user, "combined_identity_compromise", shared, steps)
    return rows

def main():
    start_time = datetime(2026, 6, 1, 9, 0, 0)

    scenarios = {
        SCENARIO_FILES["password_spray"]: build_password_spray(start_time),
        SCENARIO_FILES["brute_force"]: build_brute_force(start_time),
        SCENARIO_FILES["impossible_travel"]: build_impossible_travel(start_time),
        SCENARIO_FILES["mfa_fatigue"]: build_mfa_fatigue(start_time),
        SCENARIO_FILES["oauth_consent_abuse"]: build_oauth_consent_abuse(start_time),
        SCENARIO_FILES["mailbox_forwarding_abuse"]: build_mailbox_forwarding_abuse(start_time),
        SCENARIO_FILES["combined_identity_compromise"]: build_combined_identity_compromise(start_time)
    }

    for filename, rows in scenarios.items():
        write_csv(filename, rows)


if __name__ == "__main__":
    main()