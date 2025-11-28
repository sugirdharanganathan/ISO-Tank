from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.database import get_db
from app.models.tank_certificate import TankCertificate
from app.models.tank_header import Tank
import os
from typing import Optional, Union
from datetime import date as date_type, datetime
import traceback
import logging

# Import your shared utility functions
from app.utils.upload_utils import save_uploaded_file, delete_file_if_exists

router = APIRouter()
logger = logging.getLogger(__name__)

# Get upload root from environment or default (Same as in your other router)
UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
# Ensure upload root exists
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# Fixed Image Type for this router
CERTIFICATE_TYPE = "certificates"

# --- HELPERS ---

def clean_form_data(value: Optional[str]):
    return value.strip() if value else None

def safe_serialize_date(date_value: Union[date_type, datetime, None]) -> Optional[str]:
    if date_value and isinstance(date_value, (date_type, datetime)):
        return date_value.isoformat()
    return None

def map_form_to_payload(
    tank_id: int,
    certificate_number: str,
    insp_2_5y_date: Optional[str] = None,
    next_insp_date: Optional[str] = None,
    inspection_agency: Optional[str] = None,
    created_by: Optional[str] = "System",
    existing_file_path: Optional[str] = None
):
    try:
        insp_date = date_type.fromisoformat(insp_2_5y_date) if insp_2_5y_date else None
    except ValueError:
        insp_date = None
        
    try:
        next_date = date_type.fromisoformat(next_insp_date) if next_insp_date else None
    except ValueError:
        next_date = None
        
    return {
        "tank_id": tank_id,
        "certificate_number": clean_form_data(certificate_number),
        "insp_2_5y_date": insp_date,
        "next_insp_date": next_date,
        "inspection_agency": clean_form_data(inspection_agency),
        "created_by": clean_form_data(created_by),
        "certificate_file": existing_file_path
    }


# -------- CREATE --------
@router.post("/")
def create_tank_certificate(
    tank_id: int = Form(...),
    certificate_number: str = Form(...),
    insp_2_5y_date: Optional[str] = Form(None),
    next_insp_date: Optional[str] = Form(None),
    inspection_agency: Optional[str] = Form(None),
    certificate_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    created_by: str = Form("Admin")
):
    if not certificate_number:
        raise HTTPException(status_code=400, detail="Missing required field: certificate_number")

    # 1. Fetch Tank FIRST to get the tank_number for folder structure
    tank_record = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank_record:
        raise HTTPException(status_code=404, detail="Tank not found")
    
    tank_number = tank_record.tank_number

    # 2. Handle File Upload using shared utility
    file_path_db = None
    if certificate_file:
        try:
            # This handles: validation, temp file, folder creation, naming (tank_cert.pdf)
            file_path_db = save_uploaded_file(
                upload_file=certificate_file,
                tank_number=tank_number,
                image_type=CERTIFICATE_TYPE,
                upload_root=UPLOAD_ROOT
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # 3. Prepare Payload
    final_payload = map_form_to_payload(
        tank_id=tank_id,
        certificate_number=certificate_number,
        insp_2_5y_date=insp_2_5y_date,
        next_insp_date=next_insp_date,
        inspection_agency=inspection_agency,
        created_by=created_by,
        existing_file_path=file_path_db
    )
    
    # Add tank number to payload if your model needs it (though usually it just needs tank_id)
    final_payload['tank_number'] = tank_number
    
    cleaned_payload = {k: v for k, v in final_payload.items() if v is not None or k in ['certificate_file']}
    
    try:
        certificate = TankCertificate(**cleaned_payload)
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
    except OperationalError as op_err:
        db.rollback()
        if file_path_db:
            delete_file_if_exists(UPLOAD_ROOT, file_path_db)
        print(f"DB SCHEMA ERROR: {op_err}")
        raise HTTPException(status_code=500, detail="Database mismatch: A column might be missing.")
    except Exception as e:
        db.rollback()
        if file_path_db:
            delete_file_if_exists(UPLOAD_ROOT, file_path_db)
        print(f"INSERT ERROR: {e}")
        raise HTTPException(status_code=400, detail=f"Database Insertion Failed: {str(e)}")

    return {"message": "Tank certificate added successfully", "id": certificate.id, "file_path": file_path_db}


# -------- READ BY TANK ID --------
@router.get("/tank/{tank_id}")
def get_tank_certificates_by_tank(tank_id: int, db: Session = Depends(get_db)):
    try:
        certificates = db.query(TankCertificate).filter(
            TankCertificate.tank_id == tank_id
        ).order_by(TankCertificate.created_at.desc()).all()

        def serialize_certificate(cert):
            return {
                "id": cert.id,
                "tank_id": cert.tank_id,
                "certificate_number": cert.certificate_number,
                "insp_2_5y_date": safe_serialize_date(cert.insp_2_5y_date),
                "next_insp_date": safe_serialize_date(cert.next_insp_date),
                "year_of_manufacturing": getattr(cert, "year_of_manufacturing", "") or "",
                "inspection_agency": getattr(cert, "inspection_agency", "") or "",
                "certificate_file": cert.certificate_file or "",
                "created_at": safe_serialize_date(cert.created_at),
            }

        return [serialize_certificate(cert) for cert in certificates]

    except OperationalError as e:
        print(f"DATABASE OPERATIONAL ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Database schema error.")
    except Exception as e:
        print(f"CRITICAL ERROR in get_tank_certificates_by_tank: {str(e)}")
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail="Error retrieving certificates")


# -------- READ BY ID --------
@router.get("/{cert_id}")
def get_tank_certificate_by_id(cert_id: int, db: Session = Depends(get_db)):
    try:
        cert = db.query(TankCertificate).filter(TankCertificate.id == cert_id).first()
        if not cert:
            raise HTTPException(status_code=404, detail="Tank certificate not found")
        
        return {
            "id": cert.id,
            "tank_id": cert.tank_id,
            "certificate_number": cert.certificate_number,
            "insp_2_5y_date": safe_serialize_date(cert.insp_2_5y_date),
            "next_insp_date": safe_serialize_date(cert.next_insp_date),
            "year_of_manufacturing": getattr(cert, "year_of_manufacturing", "") or "",
            "inspection_agency": getattr(cert, "inspection_agency", "") or "",
            "certificate_file": cert.certificate_file or "",
            "created_at": safe_serialize_date(cert.created_at),
        }
    except Exception as e:
        print(f"Fetch error: {e}")
        raise HTTPException(status_code=500, detail="Error processing certificate data")


# -------- UPDATE --------
@router.put("/{cert_id}")
def update_tank_certificate(
    cert_id: int,
    certificate_number: Optional[str] = Form(None),
    insp_2_5y_date: Optional[str] = Form(None),
    next_insp_date: Optional[str] = Form(None),
    inspection_agency: Optional[str] = Form(None),
    certificate_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    updated_by: str = Form("Admin")
):
    cert = db.query(TankCertificate).filter(TankCertificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Tank certificate not found")

    # Get Tank Number for file saving
    tank_record = db.query(Tank).filter(Tank.id == cert.tank_id).first()
    if not tank_record:
         raise HTTPException(status_code=404, detail="Associated Tank not found")
    tank_number = tank_record.tank_number

    payload = {}
    if certificate_number is not None: payload["certificate_number"] = clean_form_data(certificate_number)
    
    if insp_2_5y_date is not None: 
        try:
            payload["insp_2_5y_date"] = date_type.fromisoformat(insp_2_5y_date) if insp_2_5y_date else None
        except ValueError:
            pass 
            
    if next_insp_date is not None: 
        try:
            payload["next_insp_date"] = date_type.fromisoformat(next_insp_date) if next_insp_date else None
        except ValueError:
            pass 

    if inspection_agency is not None: payload["inspection_agency"] = clean_form_data(inspection_agency)
    payload["updated_by"] = clean_form_data(updated_by)

    # File Update Logic
    if certificate_file:
        # 1. Delete old file if exists
        if cert.certificate_file:
            delete_file_if_exists(UPLOAD_ROOT, cert.certificate_file)
            
        # 2. Save new file using utility
        try:
            new_file_path = save_uploaded_file(
                upload_file=certificate_file,
                tank_number=tank_number,
                image_type=CERTIFICATE_TYPE,
                upload_root=UPLOAD_ROOT
            )
            payload["certificate_file"] = new_file_path
        except Exception as e:
             raise HTTPException(status_code=500, detail=f"New file upload failed: {str(e)}")

    try:
        for key, value in payload.items():
            if hasattr(cert, key):
                setattr(cert, key, value)
                
        db.commit()
        db.refresh(cert)
    except OperationalError as e:
        db.rollback()
        print(f"DB SCHEMA UPDATE ERROR: {e}")
        raise HTTPException(status_code=500, detail="Database schema mismatch during update.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database Update Failed: {str(e)}")
        
    return {"message": "Tank certificate updated successfully", "data": cert}


# -------- DELETE --------
@router.delete("/{cert_id}")
def delete_tank_certificate(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(TankCertificate).filter(TankCertificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Tank certificate not found")
        
    # Use utility to delete file and clean up empty folders
    if cert.certificate_file:
        delete_file_if_exists(UPLOAD_ROOT, cert.certificate_file)

    db.delete(cert)
    db.commit()
    return {"message": "Tank certificate deleted successfully"}