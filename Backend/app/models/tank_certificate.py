from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func, ForeignKey
from app.database import Base


class TankCertificate(Base):
    __tablename__ = "tank_certificate"

    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(Integer, ForeignKey("tank_header.id", ondelete="CASCADE"), nullable=False)
    tank_number = Column(String(50), ForeignKey("tank_header.tank_number"), nullable=False)
    year_of_manufacturing = Column(String(10), nullable=True)
    insp_2_5y_date = Column(Date, nullable=True)
    next_insp_date = Column(Date, nullable=True)
    certificate_number = Column(String(255), nullable=False, unique=True)
    certificate_file = Column(String(255), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

