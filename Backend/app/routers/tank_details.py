from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_header import Tank
from app.models.tank_details import TankDetails
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from io import BytesIO
from datetime import datetime

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

    # Validate status if provided
    status = data.get("status", "active")
    if status not in ["active", "inactive"]:
        raise HTTPException(status_code=400, detail="status must be 'active' or 'inactive'")
    
    # Sync status to tank_header
    tank.status = status
    db.commit()
    db.refresh(tank)
    
    tank_detail = TankDetails(
    tank_id=tank.id,
    tank_number=data["tank_number"],
    status=status,
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
        "status": r[1].status,
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

@router.get("/export-to-excel")
def export_to_excel(db: Session = Depends(get_db)):
    """
    Export all tank details to Excel file with all columns from tank_details table.
    """
    # Query all tank details with their related tank headers
    results = db.query(Tank, TankDetails).join(TankDetails, Tank.id == TankDetails.tank_id).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No tank details found to export")
    
    # Create a new workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Tank Details"
    
    # Define column headers (all columns from tank_details table)
    headers = [
        "ID",
        "Tank ID",
        "Tank Number",
        "Status",
        "Manufacturer (MFGR)",
        "Date of Manufacture",
        "PV Code",
        "UN ISO Code",
        "Capacity (L)",
        "MAWP",
        "Design Temperature",
        "Tare Weight (kg)",
        "MGW (kg)",
        "MPL (kg)",
        "Size",
        "Pump Type",
        "VESMAT",
        "Gross (kg)",
        "Net (kg)",
        "Color Body Frame",
        "Remark",
        "Lease",
        "Created By",
        "Updated By"
    ]
    
    # Style the header row
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Write data rows
    for row_num, (tank, tank_detail) in enumerate(results, 2):
        ws.cell(row=row_num, column=1, value=tank_detail.id)
        ws.cell(row=row_num, column=2, value=tank_detail.tank_id)
        ws.cell(row=row_num, column=3, value=tank_detail.tank_number or tank.tank_number)
        ws.cell(row=row_num, column=4, value=tank_detail.status)
        ws.cell(row=row_num, column=5, value=tank_detail.mfgr)
        ws.cell(row=row_num, column=6, value=tank_detail.date_mfg.strftime("%Y-%m-%d") if tank_detail.date_mfg else None)
        ws.cell(row=row_num, column=7, value=tank_detail.pv_code)
        ws.cell(row=row_num, column=8, value=tank_detail.un_iso_code)
        ws.cell(row=row_num, column=9, value=tank_detail.capacity_l)
        ws.cell(row=row_num, column=10, value=tank_detail.mawp)
        ws.cell(row=row_num, column=11, value=tank_detail.design_temperature)
        ws.cell(row=row_num, column=12, value=tank_detail.tare_weight_kg)
        ws.cell(row=row_num, column=13, value=tank_detail.mgw_kg)
        ws.cell(row=row_num, column=14, value=tank_detail.mpl_kg)
        ws.cell(row=row_num, column=15, value=tank_detail.size)
        ws.cell(row=row_num, column=16, value=tank_detail.pump_type)
        ws.cell(row=row_num, column=17, value=tank_detail.vesmat)
        ws.cell(row=row_num, column=18, value=tank_detail.gross_kg)
        ws.cell(row=row_num, column=19, value=tank_detail.net_kg)
        ws.cell(row=row_num, column=20, value=tank_detail.color_body_frame)
        ws.cell(row=row_num, column=21, value=tank_detail.remark)
        ws.cell(row=row_num, column=22, value="Yes" if tank_detail.lease else "No")
        ws.cell(row=row_num, column=23, value=tank_detail.created_by)
        ws.cell(row=row_num, column=24, value=tank_detail.updated_by)
    
    # Auto-adjust column widths
    for col_num, header in enumerate(headers, 1):
        column_letter = ws.cell(row=1, column=col_num).column_letter
        max_length = len(str(header))
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=col_num, max_col=col_num):
            if row[0].value:
                max_length = max(max_length, len(str(row[0].value)))
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)
    
    # Set row height for header
    ws.row_dimensions[1].height = 25
    
    # Save workbook to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tank_details_export_{timestamp}.xlsx"
    
    # Return as downloadable file
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@router.put("/{tank_id}")
def update_tank(tank_id: int, data: dict, db: Session = Depends(get_db)):
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    tank_detail = db.query(TankDetails).filter(TankDetails.tank_id == tank_id).first()

    if not tank or not tank_detail:
        raise HTTPException(status_code=404, detail="Tank not found")

    if "tank_number" in data:
        tank.tank_number = data["tank_number"]
        tank_detail.tank_number = data["tank_number"]  # Sync tank_number to details
    if "updated_by" in data:
        tank.updated_by = data["updated_by"]

    detail_fields = [
    "status", "mfgr", "date_mfg", "pv_code", "un_iso_code",
    "capacity_l", "mawp", "design_temperature", "tare_weight_kg",
    "mgw_kg", "mpl_kg", "size", "pump_type",
    "vesmat", "gross_kg", "net_kg", "color_body_frame",
    "remark", "lease", "updated_by"            
]

    for field in detail_fields:
      if field in data:
        if field == "lease":
            setattr(tank_detail, field, bool(data[field]))
        elif field == "status":
            # Validate status value
            if data[field] not in ["active", "inactive"]:
                raise HTTPException(status_code=400, detail="status must be 'active' or 'inactive'")
            setattr(tank_detail, field, data[field])
            # Sync status to tank_header
            tank.status = data[field]
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
        "status": tank_detail.status,
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
