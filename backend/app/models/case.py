from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base

class Case(Base):

    __tablename__ = "cases"

    upload_batch_uuid = Column(String, index= True)
    id = Column(Integer, primary_key= True, index= True)

    title = Column(String)
    status = Column(String, default="open")
    severity = Column(String)
    score = Column(Integer)

    affected_user = Column(String, index= True)
    summary = Column(Text)
    recommendations = Column(Text)
    related_alert_ids = Column(Text)

    created_at = Column(DateTime(timezone= True), server_default= func.now())
    updated_at = Column(DateTime(timezone= True), server_default= func.now())