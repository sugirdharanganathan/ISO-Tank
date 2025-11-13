from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, LoginSession
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import secrets
import hashlib
import threading

router = APIRouter()
_emp_id_lock = threading.Lock()

def generate_emp_id(db: Session) -> int:
    """Generate a unique emp_id (thread-safe)"""
    with _emp_id_lock:
        # Get the highest emp_id number
        last_user = db.query(User).order_by(User.emp_id.desc()).first()
        
        if last_user and last_user.emp_id:
            next_num = last_user.emp_id + 1
        else:
            next_num = 1
        
        # Double-check uniqueness (in case of race condition)
        while db.query(User).filter(User.emp_id == next_num).first():
            next_num += 1
        
        return next_num

def generate_salt() -> str:
    """Generate a random salt"""
    return secrets.token_hex(16)

def hash_password_with_salt(password: str, salt: str) -> str:
    """Hash password with salt using SHA256"""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, password_hash: str, password_salt: str) -> bool:
    """Verify password against hash and salt"""
    computed_hash = hash_password_with_salt(password, password_salt)
    return computed_hash == password_hash

# -----------------------------
# Pydantic Schemas
# -----------------------------
class UserRegister(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    hod: Optional[str] = None
    supervisor: Optional[str] = None
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLogout(BaseModel):
    emp_id: int

@router.post("/register")
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    Required fields: email, password
    Optional fields: name, department, designation, hod, supervisor
    emp_id is auto-generated
    """
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Generate unique emp_id
    emp_id = generate_emp_id(db)
    
    # Generate salt and hash password
    password_salt = generate_salt()
    password_hash = hash_password_with_salt(data.password, password_salt)
    
    # Create new user
    new_user = User(
        emp_id=emp_id,
        name=data.name,
        department=data.department,
        designation=data.designation,
        hod=data.hod,
        supervisor=data.supervisor,
        email=data.email,
        password_hash=password_hash,
        password_salt=password_salt
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
        "id": new_user.id,
        "emp_id": new_user.emp_id,
        "email": new_user.email,
        "name": new_user.name
    }

@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and create a session.
    Required fields: email, password
    """
    # Find user by email
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(data.password, user.password_hash, user.password_salt):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Deactivate any existing active sessions for this user
    existing_sessions = db.query(LoginSession).filter(
        LoginSession.emp_id == user.emp_id,
        LoginSession.still_logged_in == True
    ).all()
    for session in existing_sessions:
        session.still_logged_in = False
    db.commit()
    
    # Create new login session
    login_session = LoginSession(
        emp_id=user.emp_id,
        email=user.email,
        still_logged_in=True
    )
    
    db.add(login_session)
    db.commit()
    db.refresh(login_session)
    
    return {
        "message": "Login successful",
        "id": login_session.id,
        "emp_id": user.emp_id,
        "email": user.email,
        "logged_in_at": login_session.logged_in_at.isoformat() if login_session.logged_in_at else None,
        "still_logged_in": login_session.still_logged_in
    }

@router.post("/logout")
def logout_user(data: UserLogout, db: Session = Depends(get_db)):
    """
    Logout user by deactivating the session.
    Required fields: emp_id
    """
    # Find all active sessions for this emp_id
    sessions = db.query(LoginSession).filter(
        LoginSession.emp_id == data.emp_id,
        LoginSession.still_logged_in == True
    ).all()
    
    if not sessions:
        raise HTTPException(status_code=404, detail="No active session found for this user")
    
    # Deactivate all sessions
    for session in sessions:
        session.still_logged_in = False
    db.commit()
    
    return {
        "message": "Logout successful",
        "emp_id": data.emp_id
    }

