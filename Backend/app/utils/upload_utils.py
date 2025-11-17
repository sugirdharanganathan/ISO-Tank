import os
import uuid
import shutil
import logging
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException, status
from typing import Tuple

logger = logging.getLogger(__name__)

# Image type definitions
IMAGE_TYPES = {
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
}

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
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
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Only image files are allowed. Got: {file.content_type}"
        )
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image type '{file.content_type}' not supported. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )


def get_file_extension(filename: str) -> str:
    """Extract and validate file extension."""
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is empty"
        )
    
    ext = os.path.splitext(filename)[1].lower()
    if not ext or not ext.startswith('.'):
        # Default based on mime type
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
    Save uploaded file with streaming write, temp storage, and atomic rename.
    
    Args:
        upload_file: FastAPI UploadFile object
        tank_number: Tank identifier for folder structure
        image_type: Image type slug (normalized lowercase)
        upload_root: Root uploads directory path
        max_size: Maximum file size in bytes
    
    Returns:
        Relative path: tank_number/filename (forward slashes on all platforms)
    
    Raises:
        HTTPException: On validation, size, or I/O errors
    """
    try:
        # Validate inputs
        validate_file_content_type(upload_file)
        ext = get_file_extension(upload_file.filename)
        
        # Generate unique identifier
        uid = uuid.uuid4().hex
        
        # Create temp directory
        tmp_dir = os.path.join(upload_root, "tmp")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = os.path.join(tmp_dir, f"{uid}{ext}")
        
        # Stream write to temp file with size limit enforcement
        bytes_written = 0
        try:
            with open(tmp_path, "wb") as dest:
                while True:
                    chunk = upload_file.file.read(65536)  # 64KB chunks
                    if not chunk:
                        break
                    
                    bytes_written += len(chunk)
                    if bytes_written > max_size:
                        os.remove(tmp_path)
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"File size exceeds maximum allowed size of {max_size / (1024*1024):.1f}MB"
                        )
                    
                    dest.write(chunk)
        except HTTPException:
            raise
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            logger.error(f"Error writing temp file {tmp_path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error saving file"
            )
        
        # Create destination directory
        final_dir = os.path.join(upload_root, tank_number)
        os.makedirs(final_dir, exist_ok=True)
        
        # Generate final filename: tank_number_image_type_uuid.ext
        final_name = f"{tank_number}_{image_type}_{uid}{ext}"
        final_path = os.path.join(final_dir, final_name)
        
        # Atomic move (rename)
        try:
            shutil.move(tmp_path, final_path)
            # Set readable permissions
            os.chmod(final_path, 0o644)
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            logger.error(f"Error moving file to final location {final_path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error finalizing file storage"
            )
        
        # Return relative path with forward slashes
        rel_path = os.path.join(tank_number, final_name).replace("\\", "/")
        return rel_path
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in save_uploaded_file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during file upload"
        )


def delete_file_if_exists(upload_root: str, image_path: str) -> bool:
    """
    Delete a file from disk if it exists.
    
    Args:
        upload_root: Root uploads directory
        image_path: Relative path (e.g., tank_number/filename)
    
    Returns:
        True if file was deleted, False if not found
    """
    try:
        full_path = os.path.join(upload_root, image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info(f"Deleted file: {image_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {image_path}: {str(e)}")
        return False


def cleanup_temp_files(upload_root: str, hours_old: int = 2) -> int:
    """
    Clean up temporary files older than specified hours.
    
    Args:
        upload_root: Root uploads directory
        hours_old: Delete temp files older than this many hours
    
    Returns:
        Number of files deleted
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
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Cleaned up temp file: {filename}")
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {filename}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning temp directory: {str(e)}")
    
    return deleted_count


def cleanup_orphaned_files(upload_root: str, existing_paths: list) -> int:
    """
    Clean up files on disk that are not referenced in tank_images table.
    Only deletes files older than 7 days to avoid race conditions.
    
    Args:
        upload_root: Root uploads directory
        existing_paths: List of all image_path values from DB (relative paths)
    
    Returns:
        Number of files deleted
    """
    deleted_count = 0
    cutoff_time = datetime.now() - timedelta(days=7)
    
    try:
        for root, dirs, files in os.walk(upload_root):
            # Skip tmp directory
            if "tmp" in root:
                continue
            
            for filename in files:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, upload_root).replace("\\", "/")
                
                # Check if this file is referenced in DB
                if rel_path not in existing_paths:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime < cutoff_time:
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                            logger.info(f"Cleaned up orphaned file: {rel_path}")
                        except Exception as e:
                            logger.warning(f"Failed to delete orphaned file {rel_path}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning orphaned files: {str(e)}")
    
    return deleted_count
