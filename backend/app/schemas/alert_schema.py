from datetime import datetime

from pydantic import BaseModel

class AlertResponse(BaseModel):
    upload_batch_uuid: str | None
    id: int
    rule_id: str | None
    rule_name: str | None
    title: str | None
    description: str | None
    severity: str | None
    score: int | None
    affected_user: str | None
    source_ip: str | None
    mitre_technique_id: str | None
    mitre_technique_name: str | None
    evidence: str | None
    created_at: datetime | None

    class Config:
        from_attributes = True