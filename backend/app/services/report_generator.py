def generate_case_report(case):
    return f"""# Incident Report: {case.title}

## Executive Summary

{case.summary}

## Case Details

- Case ID: {case.id}
- Upload Batch UUID: {case.upload_batch_uuid}
- Severity: {case.severity}
- Score: {case.score}
- Affected User / Entity: {case.affected_user}
- Status: {case.status}

## Related Alerts

{case.related_alert_ids}

## Recommended Actions

{case.recommendations}

"""