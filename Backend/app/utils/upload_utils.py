import os
import shutil
import logging
import uuid
from typing import Tuple, Dict, Optional
from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException, status

logger = logging.getLogger(__name__)

# Image type definitions
# (I have kept your existing list, but the logic works for any type you add)
IMAGE_TYPES: Dict[str, str] = {
    "frontview": "Front View",
    "rearview": "Rear View",
    "topview": "Top View",
    "undersideview": "Underside View",
    "frontlhview": "Front Left Hand View",
    "rearlhview": "Rear Left Hand View",
    "frontrhview": "Front Right Hand View",
    "rearrhview": "Rear Right Hand View",
    "lhsideview": "Left Hand Side View",
    "rhsideview": "Right Hand Side View",
    "valvessectionview": "Valves Section View",
    "safetyvalve": "Safety Valve",
    "levelpressuregauge": "Level Pressure Gauge",
    "vacuumreading": "Vacuum Reading",
    # Add your new types here if needed:
    # "certificate": "Certificate",
    # "drawings": "Drawings", 
    # "valve_report": "Valve Report",
}

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"} 
# Added PDF just in case for reports/certificates, remove if strictly images only.

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB default


def validate_image_type(image_type: str) -> str:
    """Validate and normalize image type to lowercase."""
    normalized = image_type.lower() if image_type else ""
    if normalized not in IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image_type '{image_type}'. Allowed types: {', '.join(IMAGE_TYPES.keys())}"
        )
    return normalized


def validate_file_content_type(file: UploadFile) -> None:
    """Validate file content type and basic file validation."""
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type not provided"
        )
    
    # Optional: Allow PDF if you are doing certificates/reports
    if not (file.content_type.startswith("image/") or file.content_type == "application/pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Got: {file.content_type}"
        )
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{file.content_type}' not supported. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )


def get_file_extension(filename: str) -> str:
    """Extract and validate file extension."""
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is empty"
        )
    
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        # Default fallback
        ext = ".jpg"
    
    return ext


def save_uploaded_file(
    upload_file: UploadFile,
    tank_number: str,
    image_type: str,
    upload_root: str,
    max_size: int = MAX_UPLOAD_SIZE
) -> str:
    """
    Save uploaded file with structure: upload_root/image_type/tank_number/tank_number_image_type.ext
    """
    # --- START DEBUG BLOCK ---
    print("\n" + "="*30)
    print(f"DEBUG CHECK:")
    print(f"1. Function Called")
    print(f"2. Tank Number Received: '{tank_number}'")
    print(f"3. Image Type Received: '{image_type}'")
    print(f"4. Upload Root: '{upload_root}'")
    # --- END DEBUG BLOCK ---

    try:
        # Validate inputs
        validate_file_content_type(upload_file)
        ext = get_file_extension(upload_file.filename)
        
        # 1. Create Temp File
        uid = uuid.uuid4().hex
        tmp_dir = os.path.join(upload_root, "tmp")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = os.path.join(tmp_dir, f"{uid}{ext}")
        
        # Stream write to temp file
        bytes_written = 0
        try:
            with open(tmp_path, "wb") as dest:
                while True:
                    chunk = upload_file.file.read(65536)
                    if not chunk:
                        break
                    bytes_written += len(chunk)
                    if bytes_written > max_size:
                        dest.close()
                        os.remove(tmp_path)
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"File size exceeds limit"
                        )
                    dest.write(chunk)
        except HTTPException:
            raise
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise HTTPException(status_code=500, detail="Error saving file")
        
        # 2. Construct Target Directory
        final_dir = os.path.join(upload_root, image_type, tank_number)
        
        # --- DEBUG PRINT FOR PATH ---
        print(f"5. Target Directory Calculated: '{final_dir}'")
        print("="*30 + "\n")
        # ----------------------------

        os.makedirs(final_dir, exist_ok=True)
        
        # 3. Construct Fixed Filename
        final_name = f"{tank_number}_{image_type}{ext}"
        final_path = os.path.join(final_dir, final_name)
        
        # 4. Atomic Move
        try:
            if os.path.exists(final_path):
                os.remove(final_path)
            shutil.move(tmp_path, final_path)
            os.chmod(final_path, 0o644)
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            logger.error(f"Error moving file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error finalizing file storage")
        
        rel_path = os.path.join(image_type, tank_number, final_name).replace("\\", "/")
        return rel_path
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")


def delete_file_if_exists(upload_root: str, image_path: str) -> bool:
    """
    Delete a file from disk and clean up the tank folder if empty.
    """
    try:
        full_path = os.path.join(upload_root, image_path)
        
        if not os.path.exists(full_path):
            return False

        # Delete the file
        os.remove(full_path)
        logger.info(f"Deleted file: {image_path}")
        
        # Clean up directory if empty
        # Directory structure is: root/image_type/tank_number/file
        tank_dir = os.path.dirname(full_path) # .../uploads/frontview/TANK-1
        
        if os.path.exists(tank_dir) and not os.listdir(tank_dir):
            try:
                os.rmdir(tank_dir)
                logger.info(f"Removed empty directory: {tank_dir}")
            except OSError:
                pass # Directory might not be empty or busy, ignore
                
        return True
    except Exception as e:
        logger.error(f"Error deleting file {image_path}: {str(e)}")
        return False


def cleanup_temp_files(upload_root: str, hours_old: int = 2) -> int:
    """
    Clean up temporary files older than specified hours.
    """
    tmp_dir = os.path.join(upload_root, "tmp")
    if not os.path.exists(tmp_dir):
        return 0
    
    deleted_count = 0
    cutoff_time = datetime.now() - timedelta(hours=hours_old)
    
    try:
        for filename in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, filename)
            if os.path.isfile(file_path):
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {filename}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning temp directory: {str(e)}")
    
    return deleted_count