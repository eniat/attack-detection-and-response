from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.case import Case
from app.schemas.case_schema import CaseResponse
from app.services.case_builder import build_cases_from_alerts

router = APIRouter()

@router.get("/", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()

@router.post("/build")
def build_cases(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    case_results = build_cases_from_alerts(alerts)

    for case_data in case_results:
        db.add(Case(**case_data))
    db.commit()

    return {
        "message": "Case build complete",
        "cases_created": len(case_results),
    }