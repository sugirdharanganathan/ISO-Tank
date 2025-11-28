import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_header import Tank
from app.services.ppt_generator import create_presentation
from pydantic import BaseModel
from datetime import datetime
import traceback

router = APIRouter()

# --- CONFIGURATION ---
# UPDATED PATH: ISOTank-Mobile 1
SAVE_DIRECTORY = r"E:\ISOTank-Mobile 1\Backend\ppt"

# Ensure the folder exists immediately
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

class GenerateRequest(BaseModel):
    tank_id: int

@router.post("/generate")
def generate_ppt(payload: GenerateRequest, db: Session = Depends(get_db)):
    """
    Generates a PPT and saves it locally to E:\ISOTank-Mobile 1\Backend\ppt
    Returns a JSON success message with the file path.
    """
    try:
        # 1. Verify tank exists
        tank = db.query(Tank).filter(Tank.id == payload.tank_id).first()
        if not tank:
            raise HTTPException(status_code=404, detail="Tank not found")

        # 2. Generate the PPT (Returns BytesIO buffer)
        ppt_buffer = create_presentation(db, payload.tank_id)
        
        # 3. Create Filename and Path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Tank_Report_{tank.tank_number}_{timestamp}.pptx"
        full_save_path = os.path.join(SAVE_DIRECTORY, filename)

        # 4. Save to Server Disk
        try:
            with open(full_save_path, "wb") as f:
                f.write(ppt_buffer.getbuffer())
        except IOError as e:
            print(f"Disk Write Error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to write file to {SAVE_DIRECTORY}")

        # 5. Return JSON Success
        return JSONResponse(
            status_code=200,
            content={
                "message": "PPT generated and saved successfully.",
                "file_path": full_save_path,
                "filename": filename
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error while generating PPT")

@router.get("/history")
def get_history():
    return []