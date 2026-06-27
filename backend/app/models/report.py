from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.sql import func

from app.database import Base

class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key= True, index= True)

    case_id = Column(Integer, index= True)
    report_markdown = Column(Text)

    created_at = Column(DateTime(timezone=True),server_default=func.now())