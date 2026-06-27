from datetime import datetime

from pydantic import BaseModel

class CaseResponse(BaseModel):
    
    id: int
    title: str | None
    status: str | None
    severity: str | None
    score: int | None
    affected_user: str | None
    summary: str | None
    recommendations: str | None
    related_alert_ids: str | None
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True