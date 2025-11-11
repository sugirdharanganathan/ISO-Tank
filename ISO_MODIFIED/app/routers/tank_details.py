from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_header import Tank
from app.models.tank_details import TankDetails

router = APIRouter()

@router.post("/")
def create_tank(data: dict, db: Session = Depends(get_db)):
    required_fields = [
        "tank_number", "mfgr", "pv_code", "un_iso_code",
        "capacity_l", "mawp", "design_temperature", "tare_weight_kg",
        "mgw_kg", "mpl_kg", "size", "pump_type",
        "vesmat", "gross_kg", "net_kg", "color_body_frame"
    ]

    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"{field} is required")

    tank = Tank(
        tank_number=data["tank_number"],
        created_by=data.get("created_by")
    )
    db.add(tank)
    db.commit()
    db.refresh(tank)

    tank_detail = TankDetails(
    tank_id=tank.id,
    mfgr=data["mfgr"],
    date_mfg=data.get("date_mfg"),
    pv_code=data["pv_code"],
    un_iso_code=data["un_iso_code"],
    capacity_l=data["capacity_l"],
    mawp=data["mawp"],
    design_temperature=data["design_temperature"],
    tare_weight_kg=data["tare_weight_kg"],
    mgw_kg=data["mgw_kg"],
    mpl_kg=data["mpl_kg"],
    size=data["size"],
    pump_type=data["pump_type"],
    vesmat=data["vesmat"],
    gross_kg=data["gross_kg"],
    net_kg=data["net_kg"],
    color_body_frame=data["color_body_frame"],
    remark=data.get("remark"),                
    lease=bool(data.get("lease", 0)),       
    created_by=data.get("created_by")
)

    db.add(tank_detail)
    db.commit()
    db.refresh(tank_detail)

    return {
        "message": "Tank created successfully",
        "tank_id": tank.id,
        "data": {
            "tank_header": tank,
            "tank_details": tank_detail
        }
    }


@router.get("/")
def get_all_tanks(db: Session = Depends(get_db)):
    results = db.query(Tank, TankDetails).join(TankDetails, Tank.id == TankDetails.tank_id).all()
    
    return [
    {
        "id": r[0].id,
        "tank_number": r[0].tank_number,
        "mfgr": r[1].mfgr,
        "date_mfg": r[1].date_mfg,
        "pv_code": r[1].pv_code,
        "un_iso_code": r[1].un_iso_code,
        "capacity_l": r[1].capacity_l,
        "mawp": r[1].mawp,
        "design_temperature": r[1].design_temperature,
        "tare_weight_kg": r[1].tare_weight_kg,
        "mgw_kg": r[1].mgw_kg,
        "mpl_kg": r[1].mpl_kg,
        "size": r[1].size,
        "pump_type": r[1].pump_type,
        "vesmat": r[1].vesmat,
        "gross_kg": r[1].gross_kg,
        "net_kg": r[1].net_kg,
        "color_body_frame": r[1].color_body_frame,
        "remark": r[1].remark,                  
        "lease": int(r[1].lease),             
        "created_by": r[0].created_by
    }
    for r in results
]



@router.put("/{tank_id}")
def update_tank(tank_id: int, data: dict, db: Session = Depends(get_db)):
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    tank_detail = db.query(TankDetails).filter(TankDetails.tank_id == tank_id).first()

    if not tank or not tank_detail:
        raise HTTPException(status_code=404, detail="Tank not found")

    if "tank_number" in data:
        tank.tank_number = data["tank_number"]
    if "updated_by" in data:
        tank.updated_by = data["updated_by"]

    detail_fields = [
    "mfgr", "date_mfg", "pv_code", "un_iso_code",
    "capacity_l", "mawp", "design_temperature", "tare_weight_kg",
    "mgw_kg", "mpl_kg", "size", "pump_type",
    "vesmat", "gross_kg", "net_kg", "color_body_frame",
    "remark", "lease", "updated_by"            
]

    for field in detail_fields:
      if field in data:
        if field == "lease":
            setattr(tank_detail, field, bool(data[field])) 
        else:
            setattr(tank_detail, field, data[field])


    db.commit()
    return {"message": "Tank updated successfully"}


@router.delete("/{tank_id}")
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    tank_detail = db.query(TankDetails).filter(TankDetails.tank_id == tank_id).first()
    tank = db.query(Tank).filter(Tank.id == tank_id).first()

    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")

    if tank_detail:
        db.delete(tank_detail)
    db.delete(tank)
    db.commit()

    return {"message": "Tank deleted successfully"}

@router.get("/{tank_id}")
def get_tank_by_id(tank_id: int, db: Session = Depends(get_db)):
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    tank_detail = db.query(TankDetails).filter(TankDetails.tank_id == tank_id).first()

    if not tank or not tank_detail:
        raise HTTPException(status_code=404, detail="Tank not found")

    return {
        "id": tank.id,
        "tank_number": tank.tank_number,
        "mfgr": tank_detail.mfgr,
        "date_mfg": tank_detail.date_mfg,
        "pv_code": tank_detail.pv_code,
        "un_iso_code": tank_detail.un_iso_code,
        "capacity_l": tank_detail.capacity_l,
        "mawp": tank_detail.mawp,
        "design_temperature": tank_detail.design_temperature,
        "tare_weight_kg": tank_detail.tare_weight_kg,
        "mgw_kg": tank_detail.mgw_kg,
        "mpl_kg": tank_detail.mpl_kg,
        "size": tank_detail.size,
        "pump_type": tank_detail.pump_type,
        "vesmat": tank_detail.vesmat,
        "gross_kg": tank_detail.gross_kg,
        "net_kg": tank_detail.net_kg,
        "color_body_frame": tank_detail.color_body_frame,
        "remark": tank_detail.remark,
        "lease": int(tank_detail.lease),
        "created_by": tank.created_by,
        "updated_by": tank.updated_by,
    }

@router.get("/by-number/{tank_number}")
def get_tank_by_number(tank_number: str, db: Session = Depends(get_db)):
    tank = db.query(Tank).filter(Tank.tank_number == tank_number).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")

    tank_detail = db.query(TankDetails).filter(TankDetails.tank_id == tank.id).first()
    if not tank_detail:
        raise HTTPException(status_code=404, detail="Tank details not found")

    return {
        "tank_number": tank.tank_number,
        "date_mfg": tank_detail.date_mfg
    }
