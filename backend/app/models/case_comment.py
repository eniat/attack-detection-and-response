from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base

class CaseComment(Base):

    __tablename__ = "case_comments"

    id = Column(Integer, primary_key= True, index= True)

    case_id = Column(Integer, index= True)
    upload_batch_uuid = Column(String, index=True)

    author = Column(String, default="Analyst")
    comment = Column(Text)

    created_at = Column(DateTime(timezone= True), server_default=func.now())