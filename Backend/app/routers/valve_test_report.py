from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.valve_test_report import ValveTestReport 
from app.models.tank_header import Tank
import os
from typing import Optional
from datetime import date as date_type

# Import shared utility functions
from app.utils.upload_utils import save_uploaded_file, delete_file_if_exists

router = APIRouter()

# Get upload root from environment or default
UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# Fixed Image Type for this router
VALVE_REPORT_TYPE = "valve_reports"

def clean_form_data(value: Optional[str]):
    return value.strip() if value else None

# --- CREATE ---
@router.post("/")
def create_valve_test_report(
    tank_id: int = Form(...),
    test_date: Optional[str] = Form(None),
    inspected_by: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    inspection_report_file: Optional[UploadFile] = File(None),
    created_by: str = Form("Admin"),
    db: Session = Depends(get_db)
):
    # 1. Fetch Tank to get tank_number
    tank_record = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank_record:
        raise HTTPException(status_code=404, detail="Tank not found")
    
    tank_number = tank_record.tank_number

    # 2. Save File
    file_path_db = None
    if inspection_report_file:
        try:
            file_path_db = save_uploaded_file(
                upload_file=inspection_report_file,
                tank_number=tank_number,
                image_type=VALVE_REPORT_TYPE,
                upload_root=UPLOAD_ROOT
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    try:
        parsed_date = date_type.fromisoformat(test_date) if test_date else None
    except ValueError:
        parsed_date = None

    try:
        new_report = ValveTestReport(
            tank_id=tank_id,
            test_date=parsed_date,
            inspected_by=clean_form_data(inspected_by),
            remarks=clean_form_data(remarks),
            inspection_report_file=file_path_db,
            created_by=created_by
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
    except Exception as e:
        db.rollback()
        # Cleanup file if DB insertion fails
        if file_path_db:
            delete_file_if_exists(UPLOAD_ROOT, file_path_db)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Report created successfully", "data": new_report}

# --- READ BY TANK ID ---
@router.get("/tank/{tank_id}")
def get_valve_reports_by_tank(tank_id: int, db: Session = Depends(get_db)):
    reports = db.query(ValveTestReport).filter(ValveTestReport.tank_id == tank_id).order_by(ValveTestReport.created_at.desc()).all()
    return reports

# --- UPDATE ---
@router.put("/{report_id}")
def update_valve_test_report(
    report_id: int,
    test_date: Optional[str] = Form(None),
    inspected_by: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    inspection_report_file: Optional[UploadFile] = File(None),
    updated_by: str = Form("Admin"),
    db: Session = Depends(get_db)
):
    report = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Fetch Tank Number for file operations
    tank_record = db.query(Tank).filter(Tank.id == report.tank_id).first()
    if not tank_record:
        raise HTTPException(status_code=404, detail="Associated Tank not found")
    
    tank_number = tank_record.tank_number

    # File Update Logic
    if inspection_report_file:
        # 1. Delete old file if exists
        if report.inspection_report_file:
            delete_file_if_exists(UPLOAD_ROOT, report.inspection_report_file)
        
        # 2. Save new file
        try:
            new_file_path = save_uploaded_file(
                upload_file=inspection_report_file,
                tank_number=tank_number,
                image_type=VALVE_REPORT_TYPE,
                upload_root=UPLOAD_ROOT
            )
            report.inspection_report_file = new_file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    if test_date is not None:
        try:
            report.test_date = date_type.fromisoformat(test_date) if test_date else None
        except ValueError:
            pass
    
    if inspected_by is not None: report.inspected_by = clean_form_data(inspected_by)
    if remarks is not None: report.remarks = clean_form_data(remarks)
    report.updated_by = updated_by

    try:
        db.commit()
        db.refresh(report)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")

    return {"message": "Report updated successfully", "data": report}

# --- DELETE ---
@router.delete("/{report_id}")
def delete_valve_test_report(report_id: int, db: Session = Depends(get_db)):
    """Deletes a valve test report and its associated file."""
    report = db.query(ValveTestReport).filter(ValveTestReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Delete associated file and cleanup folders
    if report.inspection_report_file:
        delete_file_if_exists(UPLOAD_ROOT, report.inspection_report_file)

    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}