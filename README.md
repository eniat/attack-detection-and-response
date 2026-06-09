# Cloud Identity Attack Detection & Response Platform

## Problem
SOC analysts need to detect and investigate identity-based attacks from noisy authentication and audit logs.

## What it does
This platform ingests Entra ID / M365-style logs, detects suspicious identity activity, maps alerts to MITRE ATT&CK and produces analyst-ready investigation reports.

## Key detections
- Password spraying
- Brute force
- Impossible travel
- MFA fatigue
- Suspicious OAuth consent
- Suspicious mailbox forwarding

## Planned Tech Stack
- Backend: Python, FastAPI, SQLAlchemy, Pandas
- Database: PostgreSQL
- Frontend: Next.js, TypeScript, Tailwind CSS
- DevOps: Docker Compose
- Testing: Pytest

## Screenshots
Dashboard, case view, timeline, report export.

## Example scenario
A password spray attack results in one successful login, followed by suspicious mailbox forwarding. The platform links the events into one investigation case and recommends containment actions.

## Limitations
Synthetic dataset. No live Microsoft tenant integration by default. Response actions are recommendations only.
