# Cloud Identity Attack Detection & Response Platform

## Overview

Cloud Identity Detection & Response Platform is a full-stack cyber security project that detects identity-based attacks from Microsoft Entra ID / Microsoft 365-style logs.

The platform ingests CSV logs, normalises authentication and audit events, runs detection logic, maps alerts to MITRE ATT&CK, groups alerts into analyst cases, and generates Markdown incident reports.

## Why This Project Exists

Identity attacks are a common route into organisations. This project demonstrates practical skills in log analysis, detection engineering, cloud identity security, SOC investigation, and incident response reporting.

## Investigation Workflow

1. Open the Events page.
2. Use the upload controls beside the Events heading to upload a CSV log file.
3. The system creates a unique upload batch UUID.
4. The uploaded CSV appears as an event batch card.
5. Open the batch to view parsed events.
6. Run detections against that batch.
7. Build cases from the generated alerts.
8. Open a case to review the summary, recommendations, status, comments, and report.
9. Add analyst comments, update case status, and generate a Markdown incident report.

## Upload Batch Linking

Each uploaded CSV creates an `upload_batch_uuid`.

This UUID links:

- uploaded file metadata
- parsed events
- generated alerts
- analyst cases
- case comments
- reports

This keeps separate investigations isolated from each other and avoids mixing events from multiple uploads.

## Key detections
- Password spraying
- Brute force
- Impossible travel
- MFA fatigue
- Suspicious OAuth consent
- Suspicious mailbox forwarding

## Tech Stack
- Backend: Python, FastAPI, SQLAlchemy, Pandas
- Database: PostgreSQL
- Frontend: Next.js, TypeScript, Tailwind CSS
- DevOps: Docker Compose
- Testing: Pytest

## Running Locally

```bash
docker compose up --build
```

## Features

- CSV log upload
- Event normalisation
- Password spray detection
- Brute force detection
- Impossible travel detection
- MFA fatigue detection
- Suspicious OAuth consent detection
- Suspicious mailbox forwarding detection
- MITRE ATT&CK mapping
- Alert severity scoring
- Analyst case generation
- Markdown report generation
- Frontend dashboard
- Docker Compose deployment
- Pytest detection tests

## Example scenario
A password spray attack results in one successful login, followed by suspicious mailbox forwarding. The platform links the events into one investigation case and recommends containment actions.

## Limitations
Synthetic dataset. No live Microsoft tenant integration by default. Response actions are recommendations only.

## License
This project is licensed under the MIT Licence. See the `LICENSE` file for details.
