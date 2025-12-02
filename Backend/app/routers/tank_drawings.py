from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
# Ensure this matches your actual model filename
from app.models.tank_drawings import TankDrawing
from app.models.tank_header import Tank
import os
from typing import Optional
import logging

# Import shared utility functions
from app.utils.upload_utils import save_uploaded_file, delete_file_if_exists

router = APIRouter()
logger = logging.getLogger(__name__)

# Get upload root from environment or default
UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# Fixed Image Type for this router
DRAWING_TYPE = "drawings"

# --- CREATE (Upload) ---
@router.post("/")
def upload_drawing(
    tank_id: int = Form(...),
    drawing_type: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    created_by: str = Form("Admin"),
    db: Session = Depends(get_db)
):
    # 1. Fetch Tank to get tank_number for folder structure
    tank_record = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank_record:
        raise HTTPException(status_code=404, detail="Tank not found")
    
    tank_number = tank_record.tank_number

    # 2. Save File using utility
    # Structure: uploads/drawings/TANK-101/TANK-101_drawings.pdf (or similar)
    try:
        file_path_db = save_uploaded_file(
            upload_file=file,
            tank_number=tank_number,
            image_type=DRAWING_TYPE,
            upload_root=UPLOAD_ROOT
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # 3. Save DB Record
    try:
        db_drawing = TankDrawing(
            tank_id=tank_id,
            # REMOVED: tank_number=tank_number, (This caused the error)
            drawing_type=drawing_type,
            description=description.strip() if description and description.strip() else None, 
            file_path=file_path_db,
            original_filename=file.filename,
            created_by=created_by
        )
        db.add(db_drawing)
        db.commit()
        db.refresh(db_drawing)
    except Exception as e:
        # Cleanup file if DB fails
        delete_file_if_exists(UPLOAD_ROOT, file_path_db)
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Drawing uploaded successfully", "data": db_drawing}

# --- READ (List by Tank) ---
@router.get("/tank/{tank_id}")
def get_drawings_by_tank(tank_id: int, db: Session = Depends(get_db)):
    drawings = db.query(TankDrawing).filter(TankDrawing.tank_id == tank_id).order_by(TankDrawing.created_at.desc()).all()
    return drawings

# --- DELETE ---
@router.delete("/{drawing_id}")
def delete_drawing(drawing_id: int, db: Session = Depends(get_db)):
    drawing = db.query(TankDrawing).filter(TankDrawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")

    # Delete physical file and clean up empty folders
    if drawing.file_path:
        delete_file_if_exists(UPLOAD_ROOT, drawing.file_path)

    db.delete(drawing)
    db.commit()
    return {"message": "Drawing deleted successfully"}