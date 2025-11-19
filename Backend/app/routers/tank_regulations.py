from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_regulations import TankRegulation
from app.models.regulations_master import RegulationsMaster
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


# -------- CREATE --------
class TankRegulationCreate(BaseModel):
    tank_id: int
    regulation_id: int
    initial_approval_no: Optional[str] = None
    imo_type: Optional[str] = None
    safety_standard: Optional[str] = None
    regulation_name: Optional[str] = None
    country_registration: Optional[str] = None
    created_by: Optional[str] = None


class TankRegulationUpdate(BaseModel):
    tank_id: Optional[int] = None
    regulation_id: Optional[int] = None
    initial_approval_no: Optional[str] = None
    imo_type: Optional[str] = None
    safety_standard: Optional[str] = None
    regulation_name: Optional[str] = None
    country_registration: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


@router.post("/")
def create_tank_regulation(payload: TankRegulationCreate, db: Session = Depends(get_db)):
    reg = TankRegulation(
        tank_id=payload.tank_id,
        regulation_id=payload.regulation_id,
        initial_approval_no=payload.initial_approval_no,
        imo_type=payload.imo_type,
        safety_standard=payload.safety_standard,
        regulation_name=payload.regulation_name,
        country_registration=payload.country_registration,
        created_by=payload.created_by,
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return {"message": "Tank regulation added successfully", "data": reg.id}

# -------- READ ALL --------
@router.get("/")
def get_all_tank_regulations(db: Session = Depends(get_db)):
    regs = db.query(TankRegulation).all()
    return regs

# -------- READ BY TANK ID --------
@router.get("/tank/{tank_id}")
def get_tank_regulations_by_tank(tank_id: int, db: Session = Depends(get_db)):
    regs = db.query(TankRegulation, RegulationsMaster).join(
        RegulationsMaster, TankRegulation.regulation_id == RegulationsMaster.id
    ).filter(TankRegulation.tank_id == tank_id).all()

    return [
        {
            "id": r[0].id,
            "tank_id": r[0].tank_id,
            "regulation_id": r[0].regulation_id,
            "regulation_name": r[0].regulation_name or r[1].regulation_name,
            "initial_approval_no": r[0].initial_approval_no,
            "imo_type": r[0].imo_type,
            "safety_standard": r[0].safety_standard,
            "country_registration": r[0].country_registration,
            "created_by": r[0].created_by,
            "updated_by": r[0].updated_by,
            "created_at": r[0].created_at,
            "updated_at": r[0].updated_at
        }
        for r in regs
    ]

# -------- READ BY ID --------
@router.get("/{reg_id}")
def get_tank_regulation_by_id(reg_id: int, db: Session = Depends(get_db)):
    reg = db.query(TankRegulation).filter(TankRegulation.id == reg_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Tank regulation not found")
    return reg

# -------- UPDATE --------
@router.put("/{reg_id}")
def update_tank_regulation(reg_id: int, payload: TankRegulationUpdate, db: Session = Depends(get_db)):
    reg = db.query(TankRegulation).filter(TankRegulation.id == reg_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Tank regulation not found")
    for key, value in payload.dict(exclude_unset=True).items():
        if hasattr(reg, key):
            setattr(reg, key, value)
    db.commit()
    db.refresh(reg)
    return {"message": "Tank regulation updated successfully", "data": reg}

# -------- DELETE --------
@router.delete("/{reg_id}")
def delete_tank_regulation(reg_id: int, db: Session = Depends(get_db)):
    reg = db.query(TankRegulation).filter(TankRegulation.id == reg_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Tank regulation not found")
    db.delete(reg)
    db.commit()
    return {"message": "Tank regulation deleted successfully"}
