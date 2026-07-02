from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.models.upload_batch import UploadBatch
from app.schemas.event_schema import EventResponse
from app.schemas.upload_batch_schema import UploadBatchResponse

router = APIRouter()

@router.get("/",response_model= list[UploadBatchResponse])
def get_batches(db: Session = Depends(get_db)):
    return db.query(UploadBatch).order_by(UploadBatch.created_at.desc()).all()

@router.get("/{upload_batch_uuid}",response_model= UploadBatchResponse)
def get_batch(upload_batch_uuid: str, db: Session = Depends(get_db)):
    batch = (db.query(UploadBatch)
        .filter(UploadBatch.upload_batch_uuid == upload_batch_uuid)
        .first()
    )

    if not batch:
        raise HTTPException(status_code=404, detail= "Upload batch not found.")
    return batch

@router.get("/{upload_batch_uuid}/events",response_model= list[EventResponse])
def get_batch_events(upload_batch_uuid: str,db: Session = Depends(get_db)):
    return (
        db.query(Event)
        .filter(Event.upload_batch_uuid == upload_batch_uuid)
        .order_by(Event.timestamp.asc()).all()
    )