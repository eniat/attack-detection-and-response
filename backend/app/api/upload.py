from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.services.log_parser import parse_csv_upload
from app.models.upload_batch import UploadBatch

router = APIRouter()

@router.post("/")
async def upload_logs(file: UploadFile =File(...),db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail= "Only CSV files are supported")

    try:
        events = parse_csv_upload(file.file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail= str(error)) from error

    upload_batch_uuid = str(uuid4())

    batch = UploadBatch(
        upload_batch_uuid= upload_batch_uuid,
        original_filename= file.filename,
        event_count=len(events)
    )

    db.add(batch)

    for event_data in events:
        event_data["upload_batch_uuid"] = upload_batch_uuid
        db.add(Event(**event_data))

    db.commit()

    return {
        "message": "Upload successful",
        "upload_batch_uuid": upload_batch_uuid,
        "original_filename": file.filename,
        "events_imported":len(events)
    }