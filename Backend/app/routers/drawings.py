from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_drawings import TankDrawing
from app.models.tank_header import Tank
from app.utils.upload_utils import save_uploaded_file
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class DrawingCreate(BaseModel):
    tank_id: int
    drawing_type: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class DrawingUpdate(BaseModel):
    drawing_type: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


# CREATE
@router.post("/")
def create_drawing(payload: DrawingCreate, db: Session = Depends(get_db)):
    drawing = TankDrawing(
        tank_id=payload.tank_id,
        drawing_type=payload.drawing_type,
        description=payload.description,
        created_by=payload.created_by,
        updated_by=payload.updated_by,
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)
    return {"message": "Drawing created", "data": drawing}


# LIST
@router.get("/")
def list_drawings(db: Session = Depends(get_db)):
    items = db.query(TankDrawing).order_by(TankDrawing.id.desc()).all()
    return items


# GET
@router.get("/{drawing_id}")
def get_drawing(drawing_id: int, db: Session = Depends(get_db)):
    item = db.query(TankDrawing).filter(TankDrawing.id == drawing_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Drawing not found")
    return item


# UPDATE
@router.put("/{drawing_id}")
def update_drawing(drawing_id: int, payload: DrawingUpdate, db: Session = Depends(get_db)):
    item = db.query(TankDrawing).filter(TankDrawing.id == drawing_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Drawing not found")
    for key, value in payload.dict(exclude_unset=True).items():
        if hasattr(item, key) and value is not None:
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return {"message": "Drawing updated", "data": item}


# DELETE
@router.delete("/{drawing_id}")
def delete_drawing(drawing_id: int, db: Session = Depends(get_db)):
    item = db.query(TankDrawing).filter(TankDrawing.id == drawing_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Drawing not found")
    db.delete(item)
    db.commit()
    return {"message": "Drawing deleted"}


# UPLOAD FILE
@router.post("/{drawing_id}/upload")
def upload_drawing_file(
    drawing_id: int,
    file: UploadFile = File(...),
    image_type: str = Form("drawing"),
    db: Session = Depends(get_db),
):
    drawing = db.query(TankDrawing).filter(TankDrawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")

    tank = db.query(Tank).filter(Tank.id == drawing.tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Associated tank not found")

    # uploads root: <repo>/app/uploads/drawings
    repo_root = Path(__file__).resolve().parents[1]
    upload_root = os.path.join(str(repo_root), "uploads", "drawings")
    os.makedirs(upload_root, exist_ok=True)

    rel_path = save_uploaded_file(file, tank.tank_number, image_type, upload_root)

    drawing.drawing_file = rel_path
    db.commit()
    db.refresh(drawing)
    return {"message": "File uploaded", "data": drawing}
