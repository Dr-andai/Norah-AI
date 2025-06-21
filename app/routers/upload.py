from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, shutil, json
from app.db.uploads_db import insert_upload_record, fetch_all_uploads

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/files", response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    notebook: UploadFile = File(...),
    protocol: UploadFile = File(...),
    sop: UploadFile = File(...)
):
    for file, label in [(notebook, "notebook"), (protocol, "protocol"), (sop, "sop")]:
        if file.filename:
            dest_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(dest_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            insert_upload_record(file.filename, label)

    return templates.TemplateResponse("partials/upload_success.html", {
        "request": request
    })

@router.get("/ds-dashboard", response_class=HTMLResponse)
def ds_dashboard(request: Request):
    try:
        project_data = json.load(open("data/mock_project_meta.json"))
    except Exception:
        project_data = []
    
    uploads = fetch_all_uploads()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": project_data,
        "uploads": uploads,
        "role": "ds"
    })

@router.get("/upload", response_class=HTMLResponse)
def upload_view(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
