import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.case import Case
from app.models.report import Report
from app.services.report_generator import generate_case_report
from app.models.alert import Alert
from app.models.case_comment import CaseComment

router = APIRouter()

@router.post("/{case_id}")
def create_report(case_id: int,db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code= 404, detail= "Case not found.")

    try:
        related_alert_ids =json.loads(case.related_alert_ids or "[]")
    except json.JSONDecodeError:
        related_alert_ids = []

    related_alerts = (
        db.query(Alert).filter(Alert.id.in_(related_alert_ids)).all()
        if related_alert_ids
        else []
    )

    comments = (
        db.query(CaseComment)
        .filter(CaseComment.case_id == case.id)
        .order_by(CaseComment.created_at.asc()).all()
    )

    markdown = generate_case_report(case, related_alerts, comments)

    report = Report(
        case_id=case.id,
        upload_batch_uuid= case.upload_batch_uuid,
        report_markdown=markdown
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report

@router.get("/{case_id}")
def get_reports_for_case(case_id: int, db: Session = Depends(get_db)):
    return db.query(Report).filter(Report.case_id == case_id).all()