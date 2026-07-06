from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.event import Event
from app.schemas.alert_schema import AlertResponse
from app.services.detection_engine import run_all_detections
from app.models.upload_batch import UploadBatch

router = APIRouter()

@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).all()

@router.get("/batch/{upload_batch_uuid}", response_model=list[AlertResponse])
def get_alerts_for_batch(upload_batch_uuid: str,db:Session = Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.upload_batch_uuid ==upload_batch_uuid)
        .order_by(Alert.created_at.desc()).all()
    )

@router.post("/run/{upload_batch_uuid}")
def run_detections(upload_batch_uuid: str, db: Session = Depends(get_db)):

    batch = (
        db.query(UploadBatch)
        .filter(UploadBatch.upload_batch_uuid ==upload_batch_uuid)
        .first()
    )

    if not batch:
        raise HTTPException(status_code= 404, detail= "Upload batch not found")
    
    existing_alerts = (
        db.query(Alert)
        .filter(Alert.upload_batch_uuid == upload_batch_uuid)
        .count()
    )

    if existing_alerts > 0:
        return {
            "message": "Alerts already created for this upload batch",
            "upload_batch_uuid": upload_batch_uuid,
            "alerts_created": 0
        }

    events = (
        db.query(Event)
        .filter(Event.upload_batch_uuid ==upload_batch_uuid)
        .all()
    )

    alert_results = run_all_detections(events)

    for alert_data in alert_results:
        alert_data["upload_batch_uuid"] = upload_batch_uuid
        db.add(Alert(**alert_data))

    db.commit()

    return {
        "message": "Detection run complete",
        "upload_batch_uuid": upload_batch_uuid,
        "alerts_created": len(alert_results)
    }