from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)

    user_principal_name = Column(String, index=True)
    event_type = Column(String, index=True)

    ip_address = Column(String, index=True)
    country = Column(String)
    city = Column(String)

    user_agent = Column(String)
    application = Column(String)
    status = Column(String, index=True)
    failure_reason = Column(String)
    mfa_result = Column(String)
    client_app = Column(String)

    operation = Column(String, index=True)
    target_resource = Column(String)
    details = Column(Text)