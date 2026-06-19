from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.event import Event
from app.schemas.alert_schema import AlertResponse
from app.services.detection_engine import run_all_detections

router = APIRouter()

@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).all()

@router.post("/run")
def run_detections(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    alert_results = run_all_detections(events)

    for alert_data in alert_results:
        db.add(Alert(**alert_data))

    db.commit()

    return {
        "message": "Detection run complete",
        "alerts_created": len(alert_results),
    }