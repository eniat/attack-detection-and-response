from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base

class UploadBatch(Base):

    __tablename__ = "upload_batches"

    id = Column(Integer, primary_key= True, index= True)

    upload_batch_uuid = Column(String, unique= True, index= True)
    original_filename = Column(String)
    event_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone= True), server_default=func.now())