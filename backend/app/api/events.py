from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.schemas.event_schema import EventResponse

router = APIRouter()

@router.get("/",response_model= list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.timestamp.desc()).limit(500).all()