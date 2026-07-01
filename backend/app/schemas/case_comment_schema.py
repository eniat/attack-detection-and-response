from datetime import datetime

from pydantic import BaseModel

class CaseCommentCreate(BaseModel):
    comment: str
    author: str = "Analyst"

class CaseCommentResponse(BaseModel):
    id: int
    case_id: int
    upload_batch_uuid: str | None
    author: str | None
    comment: str
    created_at: datetime | None

    class Config:
        from_attributes = True