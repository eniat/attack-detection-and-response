from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base

class Alert(Base):

    __tablename__ ="alerts"

    id = Column(Integer, primary_key= True, index= True)

    rule_id = Column(String, index=True)
    rule_name = Column(String)
    title = Column(String)
    description = Column(Text)

    severity = Column(String, index= True)
    score = Column(Integer)

    affected_user = Column(String, index= True)
    source_ip = Column(String, index= True)

    mitre_technique_id = Column(String)
    mitre_technique_name = Column(String)

    evidence = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default= func.now())