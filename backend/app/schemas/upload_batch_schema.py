from datetime import datetime

from pydantic import BaseModel

class UploadBatchResponse(BaseModel):
    id: int
    upload_batch_uuid: str
    original_filename: str | None
    event_count: int | None
    created_at: datetime | None

    class Config:
        from_attributes = True