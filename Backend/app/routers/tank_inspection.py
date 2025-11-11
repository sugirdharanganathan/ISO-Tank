from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

from app.models.tank_inspection import TankInspection
from app.database import get_db

router = APIRouter()

# -----------------------------
# Pydantic Schemas
# -----------------------------
class TankInspectionBase(BaseModel):
    tank_id: Optional[int] = None
    insp_2_5y_date: Optional[date] = None
    next_insp_date: Optional[date] = None
    tank_certificate: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class TankInspectionCreate(TankInspectionBase):
    tank_id: int  # Make tank_id mandatory while creating


class TankInspectionUpdate(TankInspectionBase):
    pass


class TankInspectionResponse(TankInspectionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# -----------------------------
# CRUD Operations
# -----------------------------

# CREATE
@router.post("/", response_model=TankInspectionResponse)
def create_tank_inspection(data: TankInspectionCreate, db: Session = Depends(get_db)):
    new_record = TankInspection(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


# READ ALL
@router.get("/", response_model=List[TankInspectionResponse])
def get_all_tank_inspections(db: Session = Depends(get_db)):
    records = db.query(TankInspection).all()
    return records


# READ BY ID
@router.get("/{id}", response_model=TankInspectionResponse)
def get_tank_inspection(id: int, db: Session = Depends(get_db)):
    record = db.query(TankInspection).filter(TankInspection.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Tank inspection not found")
    return record


# UPDATE
@router.put("/{id}", response_model=TankInspectionResponse)
def update_tank_inspection(id: int, data: TankInspectionUpdate, db: Session = Depends(get_db)):
    record = db.query(TankInspection).filter(TankInspection.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Tank inspection not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    record.updated_at = datetime.now()  # Auto-update timestamp
    db.commit()
    db.refresh(record)
    return record


# DELETE
@router.delete("/{id}")
def delete_tank_inspection(id: int, db: Session = Depends(get_db)):
    record = db.query(TankInspection).filter(TankInspection.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Tank inspection not found")

    db.delete(record)
    db.commit()
    return {"detail": "Tank inspection deleted successfully"}
