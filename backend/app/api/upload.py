from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.services.log_parser import parse_csv_upload

router = APIRouter()

@router.post("/")
async def upload_logs(file: UploadFile =File(...),db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail= "Only CSV files are supported")

    try:
        events = parse_csv_upload(file.file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail= str(error)) from error

    for event_data in events:
        db.add(Event(**event_data))

    db.commit()

    return {
        "message": "Upload successful",
        "events_imported":len(events)
    }