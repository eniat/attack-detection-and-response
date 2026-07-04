from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.case import Case
from app.models.report import Report
from app.services.report_generator import generate_case_report

router = APIRouter()

@router.post("/{case_id}")
def create_report(case_id: int,db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code= 404, detail= "Case not found.")

    markdown = generate_case_report(case)

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