from datetime import datetime

from pydantic import BaseModel

class ReportResponse(BaseModel):
    id: int
    case_id: int
    report_markdown: str
    created_at: datetime | None

    class Config:
        from_attributes = True