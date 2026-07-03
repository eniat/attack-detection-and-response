from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.alert import Alert
from app.models.case import Case
from app.schemas.case_schema import CaseResponse
from app.services.case_builder import build_cases_from_alerts
from app.models.case_comment import CaseComment

router = APIRouter()

class CaseStatusUpdate(BaseModel):
    status: str

class CaseCommentCreate(BaseModel):
    comment: str

@router.get("/", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()

@router.get("/by-batch/{upload_batch_uuid}", response_model= list[CaseResponse])
def get_cases_by_batch(upload_batch_uuid: str,db:Session = Depends(get_db)):
    return (
        db.query(Case)
        .filter(Case.upload_batch_uuid ==upload_batch_uuid)
        .order_by(Case.created_at.desc()).all()
    )

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

@router.post("/build/{upload_batch_uuid}")
def build_cases_by_batch(upload_batch_uuid: str,db:Session = Depends(get_db)):
    alerts = (
        db.query(Alert)
        .filter(Alert.upload_batch_uuid ==upload_batch_uuid)
        .all()
    )

    case_results = build_cases_from_alerts(alerts)

    for case_data in case_results:
        case_data["upload_batch_uuid"] = upload_batch_uuid
        db.add(Case(**case_data))

    db.commit()

    return {
        "message": "Case build complete",
        "upload_batch_uuid": upload_batch_uuid,
        "cases_created": len(case_results)
    }

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case


@router.patch("/{case_id}/status", response_model=CaseResponse)
def update_case_status(case_id: int, status_update: CaseStatusUpdate,db:Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code= 404, detail= "Case not found")

    case.status = status_update.status
    db.commit()
    db.refresh(case)
    return case

@router.get("/{case_id}/comments")
def get_case_comments(case_id: int,db:Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code= 404, detail= "Case not found")

    return (
        db.query(CaseComment)
        .filter(CaseComment.case_id == case_id)
        .order_by(CaseComment.created_at.asc()).all()
    )

@router.post("/{case_id}/comments")
def add_case_comment(case_id: int, comment_data: CaseCommentCreate,db:Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code= 404, detail= "Case not found")

    comment = CaseComment(case_id= case_id, comment= comment_data.comment)

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment