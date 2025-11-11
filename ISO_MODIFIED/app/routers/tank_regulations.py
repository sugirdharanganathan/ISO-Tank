from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_regulations import TankRegulation
from app.models.regulations_master import RegulationsMaster

router = APIRouter()

# -------- CREATE --------
@router.post("/")
def create_tank_regulation(payload: dict, db: Session = Depends(get_db)):
    required_fields = ["tank_id", "regulation_id"]
    for f in required_fields:
        if f not in payload:
            raise HTTPException(status_code=400, detail=f"Missing field: {f}")
    reg = TankRegulation(**payload)
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
            "regulation_name": r[1].regulation_name,
            "initial_approval_no": r[0].initial_approval_no,
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
def update_tank_regulation(reg_id: int, payload: dict, db: Session = Depends(get_db)):
    reg = db.query(TankRegulation).filter(TankRegulation.id == reg_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Tank regulation not found")
    for key, value in payload.items():
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
