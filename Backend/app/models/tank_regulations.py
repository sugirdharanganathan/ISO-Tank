from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from app.database import Base

class TankRegulation(Base):
    __tablename__ = "tank_regulations"

    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(Integer, ForeignKey("tank_header.id", ondelete="CASCADE"))
    regulation_id = Column(Integer, ForeignKey("regulations_master.id", ondelete="CASCADE"))
    initial_approval_no = Column(String(100), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
