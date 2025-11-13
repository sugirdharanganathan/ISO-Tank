from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    designation = Column(String(255), nullable=True)
    hod = Column(String(255), nullable=True)
    supervisor = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    password_salt = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("users.emp_id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    logged_in_at = Column(TIMESTAMP, server_default=func.now())
    still_logged_in = Column(Boolean, default=True, nullable=False)

