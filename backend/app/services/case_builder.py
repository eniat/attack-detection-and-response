import json

from collections import defaultdict

def build_cases_from_alerts(alerts, upload_batch_uuid: str):

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

        title = f"Identity Investigation  - {key}"

        summary =(
            f"{len(related_alerts)} related alert(s) were identified in upload: "
            f"{upload_batch_uuid}: {', '.join(alert_names)}."
        )

        recommendations = build_case_recommendations(related_alerts)

        cases.append({
            "upload_batch_uuid": upload_batch_uuid,
            "title": title,
            "status": "open",
            "severity": severity,
            "score": max_score,
            "affected_user": key,
            "summary":summary,
            "recommendations": recommendations,
            "related_alert_ids": json.dumps(related_ids)
        })

    return cases

def build_case_recommendations(related_alerts):
    rule_ids = {alert.rule_id for alert in related_alerts}

    recommendations = []

    if "DET-001" in rule_ids:
        recommendations.extend([
            "Review failed sign-in activity across all affected users in the upload batch.",
            "Block or investigate the source IP associated with the password spray activity.",
            "Check whether any targeted accounts later had successful sign-ins.",
            "Require password resets for accounts that show signs of compromise.",
            "Confirm MFA is enabled and enforced for affected users."
        ])

    if "DET-002" in rule_ids:
        recommendations.extend([
            "Review the targeted account for repeated failed authentication attempts.",
            "Reset the affected user's password if the activity was not expected.",
            "Revoke active sessions for the affected account.",
            "Review account lockout and conditional access controls.",
            "Investigate the source IP for additional authentication attempts."
        ])

    if "DET-003" in rule_ids:
        recommendations.extend([
            "Confirm whether the user could realistically have signed in from both locations.",
            "Revoke active sessions if the travel pattern cannot be explained.",
            "Reset the affected user's password if account compromise is suspected.",
            "Review MFA prompts, device information, and recent successful sign-ins.",
            "Check for follow-on activity such as mailbox rule creation or OAuth consent."
        ])

    if "DET-004" in rule_ids:
        recommendations.extend([
            "Review MFA prompt history for repeated denials followed by approval.",
            "Contact the affected user to confirm whether they approved the MFA request.",
            "Revoke active sessions and require the user to re-authenticate.",
            "Reset credentials if the approval was suspicious or unexpected.",
            "Consider re-registering MFA methods for the affected account."
        ])

    if "DET-005" in rule_ids:
        recommendations.extend([
            "Review the OAuth application that was granted access.",
            "Revoke suspicious OAuth consent grants from the affected account.",
            "Check whether high-risk permissions such as Mail.Read or offline_access were granted.",
            "Review mailbox, file, and application access performed by the OAuth app.",
            "Restrict user consent to applications where appropriate."
        ])

    if "DET-006" in rule_ids:
        recommendations.extend([
            "Review and remove suspicious mailbox forwarding or inbox rules.",
            "Check the external forwarding address for signs of data exfiltration.",
            "Review mailbox audit logs for message access or rule changes.",
            "Reset credentials and revoke sessions if the rule was not created by the user.",
            "Check for related OAuth consent or successful suspicious sign-ins."
        ])

    if not recommendations:
        recommendations.extend([
            "Review the related alerts and authentication history.",
            "Revoke active sessions if compromise is suspected.",
            "Reset credentials for affected users where appropriate.",
            "Review MFA status and recent sign-in activity.",
            "Check mailbox and OAuth activity for follow-on compromise."
        ])

    unique_recommendations = list(dict.fromkeys(recommendations))

    return "\n".join(f"- {recommendation}" for recommendation in unique_recommendations)

def get_case_severity(score):
    if score >= 90:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"