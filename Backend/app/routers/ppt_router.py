import os
import traceback
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tank_header import Tank
from app.services.ppt_generator import create_presentation
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# --- CONFIGURATION (DYNAMIC PATHS) ---
# Get the absolute path of the current file's directory (app/routers)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get the Project Root (Backend folder)
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

# Define save directory relative to project root
SAVE_DIRECTORY = os.path.join(BASE_DIR, "uploads", "ppt")

# Ensure the folder exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

class GenerateRequest(BaseModel):
    tank_id: int

@router.post("/generate")
def generate_ppt(payload: GenerateRequest, db: Session = Depends(get_db)):
    """
    Generates a PPT and saves it locally to /Backend/uploads/ppt
    Returns a JSON success message with the file path.
    """
    try:
        # --- DEBUG LOGGING ---
        print(f"DEBUG: Generating for Tank ID: {payload.tank_id}")
        print(f"DEBUG: BASE_DIR is: {BASE_DIR}")
        print(f"DEBUG: SAVE_DIRECTORY is: {SAVE_DIRECTORY}")

        # 1. Verify tank exists
        tank = db.query(Tank).filter(Tank.id == payload.tank_id).first()
        if not tank:
            raise HTTPException(status_code=404, detail=f"Tank with ID {payload.tank_id} not found")

        # 2. Generate the PPT (Returns BytesIO buffer)
        # We pass BASE_DIR so the generator knows where to look for images
        ppt_buffer = create_presentation(db, payload.tank_id, BASE_DIR)
        
        # 3. Create Filename and Path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Tank_Report_{tank.tank_number}_{timestamp}.pptx"
        full_save_path = os.path.join(SAVE_DIRECTORY, filename)

        # 4. Save to Server Disk
        try:
            with open(full_save_path, "wb") as f:
                f.write(ppt_buffer.getbuffer())
        except IOError as e:
            print(f"ERROR: Disk Write Failed: {e}")
            # This specific error usually means folder permissions are missing
            raise HTTPException(status_code=500, detail=f"Permission denied or path missing: {SAVE_DIRECTORY}")

        # 5. Return JSON Success
        return JSONResponse(
            status_code=200,
            content={
                "message": "PPT generated and saved successfully.",
                "file_path": full_save_path,
                "filename": filename
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like the 404 above) so they pass through
        raise
    except ValueError as e:
        # Catch value errors from the generator
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # CRITICAL: Print the real error to logs
        print("CRITICAL SERVER ERROR:")
        traceback.print_exc()
        # CRITICAL: Send the real error to Frontend for debugging
        raise HTTPException(status_code=500, detail=f"Debug Error: {str(e)}")