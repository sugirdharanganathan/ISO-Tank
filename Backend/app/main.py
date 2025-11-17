from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

from app.database import engine, Base
from app.routers import tank_details , regulations_master , tank_regulations , cargo_tank , cargo_master , tank_inspection, auth, users, upload

load_dotenv()
UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", os.path.join(os.path.dirname(__file__), "..", "uploads"))
os.makedirs(UPLOAD_ROOT, exist_ok=True)

app = FastAPI(
    title="ISO TANKS MANAGEMENT",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(
    tank_details.router,
    prefix="/api/tank-details",
    tags=["Tank Details"]
)

app.include_router(
    regulations_master.router,
    prefix="/api/regulations",
    tags=["Regulations"]
)

app.include_router(
    tank_regulations.router,
    prefix="/api/regulations_tank",
    tags=["Regulations tank"]
)


app.include_router(
    cargo_tank.router,
    prefix="/api/cargo_tank",
    tags=["Cargo Tank"])

app.include_router(
    cargo_master.router,
    prefix="/api/cargo_tank_master",
    tags=["Cargo Tank Master"])

app.include_router(
    tank_inspection.router,
    prefix="/api/inspections",
    tags=["Inspections"])

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Auth"])

app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"])

app.include_router(
    upload.router,
    prefix="/api/upload",
    tags=["Upload"])

@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("tank_management.html", {"request": request})

