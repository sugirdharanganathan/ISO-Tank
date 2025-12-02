from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, Text
from app.database import Base

class TankDrawing(Base):
    __tablename__ = "tank_drawings"

    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(Integer, ForeignKey("tank_header.id", ondelete="CASCADE"), nullable=False)
    
    drawing_type = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Stores the local file path relative to the backend
    file_path = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    
    created_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())