from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.valve_test_report import ValveTestReport
from app.models.tank_header import Tank
from app.utils.upload_utils import save_uploaded_file
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ValveReportCreate(BaseModel):
    tank_id: int
    test_date: Optional[str] = None
    inspected_by: Optional[str] = None
    remarks: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class ValveReportUpdate(BaseModel):
    test_date: Optional[str] = None
    inspected_by: Optional[str] = None
    remarks: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


@router.post("/")
def create_valve_report(payload: ValveReportCreate, db: Session = Depends(get_db)):
    rpt = ValveTestReport(
        tank_id=payload.tank_id,
        test_date=payload.test_date,
        inspected_by=payload.inspected_by,
        remarks=payload.remarks,
        created_by=payload.created_by,
        updated_by=payload.updated_by,
    )
    db.add(rpt)
    db.commit()
    db.refresh(rpt)
    return {"message": "Valve test report created", "data": rpt}


# LIST
@router.get("/")
def list_valve_reports(db: Session = Depends(get_db)):
    items = db.query(ValveTestReport).order_by(ValveTestReport.id.desc()).all()
    return items


# GET
@router.get("/{report_id}")
def get_valve_report(report_id: int, db: Session = Depends(get_db)):
    item = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Valve test report not found")
    return item


# UPDATE
@router.put("/{report_id}")
def update_valve_report(report_id: int, payload: ValveReportUpdate, db: Session = Depends(get_db)):
    item = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Valve test report not found")
    for key, value in payload.dict(exclude_unset=True).items():
        if hasattr(item, key) and value is not None:
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return {"message": "Valve test report updated", "data": item}


# DELETE
@router.delete("/{report_id}")
def delete_valve_report(report_id: int, db: Session = Depends(get_db)):
    item = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Valve test report not found")
    db.delete(item)
    db.commit()
    return {"message": "Valve test report deleted"}


# UPLOAD FILE
@router.post("/{report_id}/upload")
def upload_inspection_report(
    report_id: int,
    file: UploadFile = File(...),
    image_type: str = Form("inspection_report"),
    db: Session = Depends(get_db),
):
    rpt = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not rpt:
        raise HTTPException(status_code=404, detail="Valve test report not found")

    tank = db.query(Tank).filter(Tank.id == rpt.tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Associated tank not found")

    repo_root = Path(__file__).resolve().parents[1]
    upload_root = os.path.join(str(repo_root), "uploads", "valve_reports")
    os.makedirs(upload_root, exist_ok=True)

    rel_path = save_uploaded_file(file, tank.tank_number, image_type, upload_root)

    rpt.inspection_report_file = rel_path
    db.commit()
    db.refresh(rpt)
    return {"message": "File uploaded", "data": rpt}
