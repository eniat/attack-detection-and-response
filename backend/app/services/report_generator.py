from datetime import datetime, timezone

def format_related_alerts(related_alerts):
    if not related_alerts:
        return "No related alert details available."

    alert_sections = []

    for alert in related_alerts:
        alert_sections.append(
            f"""### Alert {alert.id} — {alert.rule_name}

- Rule ID: {alert.rule_id}
- Title: {alert.title}
- Severity: {alert.severity}
- Score: {alert.score}
- Affected User / Entity: {alert.affected_user}
- Source IP: {alert.source_ip}
- MITRE Technique: {alert.mitre_technique_id} — {alert.mitre_technique_name}
- Created At: {alert.created_at}

**Evidence**

{alert.evidence}
"""
        )

    return "\n".join(alert_sections)


def format_analyst_comments(comments):
    if not comments:
        return "No analyst comments recorded."

    return "\n".join(
        f"- {comment.created_at}: {comment.comment}"
        for comment in comments
    )


def generate_case_report(case, related_alerts=None, comments=None):
    related_alerts = related_alerts or []
    comments = comments or []

    generated_at = datetime.now(timezone.utc).isoformat()

    return f"""# Incident Report: {case.title}

## Executive Summary

{case.summary}

## Report Metadata

- Generated At: {generated_at}
- Case ID: {case.id}
- Upload Batch UUID: {case.upload_batch_uuid}
- Current Status: {case.status}

## Case Details

- Severity: {case.severity}
- Score: {case.score}
- Affected User / Entity: {case.affected_user}
- Related Alert IDs: {case.related_alert_ids}

## Detection Summary

This case contains {len(related_alerts)} related alert(s). The alerts below provide the detection logic, MITRE ATT&CK mapping, source indicators, affected entity, and supporting evidence.

## Related Alerts

{format_related_alerts(related_alerts)}

## Analyst Comments

{format_analyst_comments(comments)}

## Recommended Actions

{case.recommendations}

"""