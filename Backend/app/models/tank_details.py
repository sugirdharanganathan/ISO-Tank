from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Date
from app.database import Base

class TankDetails(Base):
    __tablename__ = "tank_details"

    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(Integer, ForeignKey("tank_header.id"))
    tank_number = Column(String(50), ForeignKey("tank_header.tank_number"), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    mfgr = Column(String(255))
    date_mfg = Column(Date, nullable=True)
    pv_code = Column(String(255))
    un_iso_code = Column(String(255))
    capacity_l = Column(Float)
    mawp = Column(Float)
    design_temperature = Column(String(50), nullable=True)
    tare_weight_kg = Column(Float)
    mgw_kg = Column(Float)
    mpl_kg = Column(Float)
    size = Column(String(100))
    pump_type = Column(String(100))
    vesmat = Column(String(255))
    gross_kg = Column(Float)
    net_kg = Column(Float)
    color_body_frame = Column(String(255))
    working_pressure = Column(Float, nullable=True)
    cabinet_type = Column(String(100), nullable=True)
    frame_type = Column(String(100), nullable=True)
    
    remark = Column(Text, nullable=True)
    lease = Column(Boolean, default=False)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)