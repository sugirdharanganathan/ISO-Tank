from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tank_certificate import TankCertificate
from app.models.tank_header import Tank
from app.utils.upload_utils import save_uploaded_file
import os
from pathlib import Path

router = APIRouter()


# ==================== Schemas ====================

class TankCertificateBase(BaseModel):
    tank_number: str
    year_of_manufacturing: Optional[str] = None
    insp_2_5y_date: Optional[date] = None
    next_insp_date: Optional[date] = None
    certificate_number: str
    certificate_file: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class TankCertificateCreate(TankCertificateBase):
    pass


class TankCertificateUpdate(BaseModel):
    tank_number: Optional[str] = None
    year_of_manufacturing: Optional[str] = None
    insp_2_5y_date: Optional[date] = None
    next_insp_date: Optional[date] = None
    certificate_number: Optional[str] = None
    certificate_file: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class TankCertificateResponse(BaseModel):
    id: int
    tank_id: int
    tank_number: str
    year_of_manufacturing: Optional[str] = None
    insp_2_5y_date: Optional[date] = None
    next_insp_date: Optional[date] = None
    certificate_number: str
    certificate_file: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Helpers ====================

def _get_tank_by_number(db: Session, tank_number: str) -> Tank:
    tank = db.query(Tank).filter(Tank.tank_number == tank_number).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank


def _ensure_unique_certificate_number(
    db: Session, certificate_number: str, current_id: Optional[int] = None
):
    query = db.query(TankCertificate).filter(
        TankCertificate.certificate_number == certificate_number
    )
    if current_id is not None:
        query = query.filter(TankCertificate.id != current_id)
    if query.first():
        raise HTTPException(status_code=400, detail="Certificate number already exists")


# ==================== Endpoints ====================

@router.post("/", response_model=TankCertificateResponse)
def create_certificate(
    data: TankCertificateCreate, db: Session = Depends(get_db)
):
    tank = _get_tank_by_number(db, data.tank_number)
    _ensure_unique_certificate_number(db, data.certificate_number)

    certificate = TankCertificate(
        tank_id=tank.id,
        tank_number=tank.tank_number,
        year_of_manufacturing=data.year_of_manufacturing,
        insp_2_5y_date=data.insp_2_5y_date,
        next_insp_date=data.next_insp_date,
        certificate_number=data.certificate_number,
        certificate_file=data.certificate_file,
        created_by=data.created_by,
        updated_by=data.updated_by,
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate


@router.get("/", response_model=List[TankCertificateResponse])
def list_certificates(db: Session = Depends(get_db)):
    certificates = (
        db.query(TankCertificate)
        .order_by(TankCertificate.id.desc())
        .all()
    )
    return certificates


@router.get("/{certificate_id}", response_model=TankCertificateResponse)
def get_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = (
        db.query(TankCertificate)
        .filter(TankCertificate.id == certificate_id)
        .first()
    )
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate


@router.put("/{certificate_id}", response_model=TankCertificateResponse)
def update_certificate(
    certificate_id: int, data: TankCertificateUpdate, db: Session = Depends(get_db)
):
    certificate = (
        db.query(TankCertificate)
        .filter(TankCertificate.id == certificate_id)
        .first()
    )
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    if data.tank_number is not None:
        tank = _get_tank_by_number(db, data.tank_number)
        certificate.tank_id = tank.id
        certificate.tank_number = tank.tank_number

    if data.certificate_number is not None:
        _ensure_unique_certificate_number(
            db, data.certificate_number, current_id=certificate.id
        )
        certificate.certificate_number = data.certificate_number

    update_payload = data.dict(exclude_unset=True, exclude={"tank_number", "certificate_number"})

    for field, value in update_payload.items():
        setattr(certificate, field, value)

    db.commit()
    db.refresh(certificate)
    return certificate


@router.delete("/{certificate_id}")
def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = (
        db.query(TankCertificate)
        .filter(TankCertificate.id == certificate_id)
        .first()
    )
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    db.delete(certificate)
    db.commit()
    return {"message": "Certificate deleted successfully"}


@router.post("/{certificate_id}/upload", response_model=TankCertificateResponse)
def upload_certificate_file(
    certificate_id: int,
    file: UploadFile = File(...),
    image_type: str = Form("frontview"),
    db: Session = Depends(get_db),
):
    """Upload a certificate image and save its relative path to `certificate_file` column.

    The file is stored under `uploads/certificates/<tank_number>/...` and the DB
    record is updated with the relative path (forward slashes).
    """
    # Find certificate
    certificate = db.query(TankCertificate).filter(TankCertificate.id == certificate_id).first()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # Ensure tank exists (to derive tank_number folder)
    tank = db.query(Tank).filter(Tank.id == certificate.tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Associated tank not found")

    # Resolve uploads root: <project>/app/uploads/certificates
    repo_root = Path(__file__).resolve().parents[1]
    upload_root = os.path.join(str(repo_root), "uploads", "certificates")
    os.makedirs(upload_root, exist_ok=True)

    # Normalize image_type and save
    saved_rel_path = save_uploaded_file(file, tank.tank_number, image_type, upload_root)

    # Update DB record with relative path
    certificate.certificate_file = saved_rel_path
    db.commit()
    db.refresh(certificate)

    return certificate

