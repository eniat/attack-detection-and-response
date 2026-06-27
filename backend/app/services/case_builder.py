import json

from collections import defaultdict

def build_cases_from_alerts(alerts):

    grouped_alerts = defaultdict(list)

    for alert in alerts:
        key = alert.affected_user if alert.affected_user !="multiple" else alert.source_ip
        grouped_alerts[key].append(alert)

    cases = []

    for key, related_alerts in grouped_alerts.items():
        max_score = max(alert.score for alert in related_alerts)
        severity = get_case_severity(max_score)

        related_ids = [alert.id for alert in related_alerts]
        alert_names = [alert.rule_name for alert in related_alerts]

        title = f"Identity Security Case - {key}"

        summary =(
            f"{len(related_alerts)} related alert(s) were identified for {key}: "
            f"{', '.join(alert_names)}."
        )

        recommendations = [
            "Review authentication history.",
            "Revoke active sessions if compromise is suspected.",
            "Reset credentials for affected users.",
            "Review MFA status.",
            "Check mailbox and OAuth activity."
        ]

        cases.append({
            "title": title,
            "status": "open",
            "severity": severity,
            "score": max_score,
            "affected_user": key,
            "summary":summary,
            "recommendations": json.dumps(recommendations),
            "related_alert_ids": json.dumps(related_ids)
        })

    return cases

def get_case_severity(score):
    if score >= 90:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"