from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class TankDrawing(Base):
    __tablename__ = "tank_drawings"

    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(Integer, ForeignKey("tank_header.id", ondelete="CASCADE"), nullable=False)
    drawing_type = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    drawing_file = Column(String(255), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    tank = relationship("Tank", foreign_keys=[tank_id], lazy="joined")
