from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy import text
from app.database import init_db, get_db, engine, SessionLocal # <--- Added SessionLocal
from app.seed import init_seed_data # <--- Import the seeding function

from app.routers import (
    auth, users, 
    tank_details, tank_inspection, 
    tank_regulations, regulations_master,
    cargo_master, cargo_tank,
    upload, tank_certificate, tank_drawings,
    valve_test_report,
    ppt_router
)

app = FastAPI(title="ISO-TANK API")

# --- CORS MIDDLEWARE ---
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# --- ROUTERS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tank_details.router, prefix="/api/tanks", tags=["Tanks"]) 
app.include_router(tank_inspection.router, prefix="/api/tank-inspection", tags=["Tank Inspection"])
app.include_router(tank_certificate.router, prefix="/api/tank-certificates", tags=["Tank Certificates"])
app.include_router(tank_regulations.router, prefix="/api/tank-regulations", tags=["Tank Regulations"])
app.include_router(regulations_master.router, prefix="/api/regulations-master", tags=["Regulations Master"])
app.include_router(cargo_master.router, prefix="/api/cargo-master", tags=["Cargo Master"])
app.include_router(cargo_tank.router, prefix="/api/cargo-tank", tags=["Cargo Tank"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(tank_drawings.router, prefix="/api/tank-drawings", tags=["Tank Drawings"])
app.include_router(valve_test_report.router, prefix="/api/valve-test-reports", tags=["Valve Test Reports"])
app.include_router(ppt_router.router, prefix="/api/ppt", tags=["PPT Generation"])

# --- STARTUP EVENT ---
@app.on_event("startup")
def on_startup():
    # 1. Initialize standard tables
    init_db()
    
    # 2. AUTO-FIX: Add 'inspection_agency' column if it's missing
    with engine.connect() as conn:
        try:
            print("Checking database schema for missing columns...")
            conn.execute(text("ALTER TABLE tank_certificate ADD COLUMN inspection_agency VARCHAR(10) NULL;"))
            conn.commit()
            print("SUCCESS: Added missing column 'inspection_agency' to table 'tank_certificate'.")
            
        except Exception as e:
            # This is expected if the column already exists
            print(f"Schema check passed (or column exists): {e}")

    # 3. SEEDING: Insert initial values for Master tables
    # We use a separate SessionLocal just for this operation
    db = SessionLocal()
    try:
        print("Checking for seed data...")
        init_seed_data(db)
        print("Seeding check completed.")
    except Exception as e:
        print(f"Error during seeding: {e}")
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}