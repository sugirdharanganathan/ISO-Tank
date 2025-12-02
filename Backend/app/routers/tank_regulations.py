from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.database import get_db
from app.models.tank_regulations import TankRegulation
from app.models.regulations_master import RegulationsMaster

router = APIRouter()

# --- NOTE: Removed get_or_create_regulation_master helper, as frontend sends ID ---

# -------- CREATE --------
@router.post("/")
def create_tank_regulation(payload: dict, db: Session = Depends(get_db)):
    # FIX: Revert required field check to look for regulation_id (the dropdown value)
    required_fields = ["tank_id", "regulation_id"] 
    for f in required_fields:
        # Check for presence and ensure regulation_id is not empty/null (i.e., the placeholder '-- Choose --' wasn't selected)
        if f not in payload or not payload[f]:
            raise HTTPException(status_code=400, detail=f"Missing or empty required field: {f}")

    # Initialize final payload by cleaning optional string fields (imo_type, etc.)
    final_payload = {}
    for key, value in payload.items():
        # Convert empty strings to None for optional fields before SQLAlchemy receives them
        final_payload[key] = value if value != "" else None
    
    # Ensure mandatory fields are present
    if 'tank_id' not in final_payload:
        final_payload['tank_id'] = payload['tank_id']
    if 'regulation_id' not in final_payload:
        final_payload['regulation_id'] = payload['regulation_id']

    # --- REMOVED COMPLEX NAME LOOKUP LOGIC ---

    # 4. Create Tank Regulation record
    try:
        reg = TankRegulation(**final_payload)
        db.add(reg)
        db.commit()
        db.refresh(reg)
    except Exception as e:
        db.rollback()
        import logging
        logging.error(f"SQLAlchemy Insertion Error: {e}")
        raise HTTPException(status_code=400, detail=f"Database Insertion Failed. Check model constraints. Detail: {str(e)}")

    return {"message": "Tank regulation added successfully", "data": reg.id}

# -------- READ ALL (Kept Fixes for retrieval/display) --------
@router.get("/")
def get_all_tank_regulations(db: Session = Depends(get_db)):
    regs = db.query(TankRegulation, RegulationsMaster).outerjoin(
        RegulationsMaster, TankRegulation.regulation_id == RegulationsMaster.id
    ).all()
    
    return [
        {
            "id": r[0].id,
            "tank_id": r[0].tank_id,
            "regulation_id": r[0].regulation_id,
            "regulation_name": r[1].regulation_name if r[1] else r[0].regulation_name, # Use Master name first
            
            # Retrieval Fix: Ensure None values are explicitly converted to empty strings for the frontend
            "initial_approval_no": r[0].initial_approval_no or "",
            "imo_type": r[0].imo_type or "",
            "safety_standard": r[0].safety_standard or "",
            "country_registration": r[0].country_registration or "",
            
            "created_by": r[0].created_by,
            "updated_by": r[0].updated_by,
            "created_at": r[0].created_at,
            "updated_at": r[0].updated_at
        }
        for r in regs
    ]

# -------- READ BY TANK ID (Kept Fixes for retrieval/display) --------
@router.get("/tank/{tank_id}")
def get_tank_regulations_by_tank(tank_id: int, db: Session = Depends(get_db)):
    regs = db.query(TankRegulation, RegulationsMaster).outerjoin(
        RegulationsMaster, TankRegulation.regulation_id == RegulationsMaster.id
    ).filter(TankRegulation.tank_id == tank_id).all()

    return [
        {
            "id": r[0].id,
            "tank_id": r[0].tank_id,
            "regulation_id": r[0].regulation_id,
            "regulation_name": r[1].regulation_name if r[1] else r[0].regulation_name, # Use Master name first
            
            # Retrieval Fix: Ensure None values are explicitly converted to empty strings for the frontend
            "initial_approval_no": r[0].initial_approval_no or "",
            "imo_type": r[0].imo_type or "",
            "safety_standard": r[0].safety_standard or "",
            "country_registration": r[0].country_registration or "",
            
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
    
    # Clean payload for update
    cleaned_payload = {}
    for key, value in payload.items():
        # Convert empty strings to None before update
        cleaned_payload[key] = value if value != "" else None

    for key, value in cleaned_payload.items():
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