from datetime import datetime

from pydantic import BaseModel


class EventResponse(BaseModel):
    id: int
    event_id: str | None
    timestamp: datetime | None
    user_principal_name: str | None
    event_type: str | None
    ip_address: str | None
    country: str | None
    city: str | None
    application: str | None
    status: str | None
    operation: str | None

    class Config:
        from_attributes = True