from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, shutil, json

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
    for file in [notebook, protocol, sop]:
        dest_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "message": "✅ Files uploaded successfully."
    })

@router.get("/ds-dashboard", response_class=HTMLResponse)
def ds_dashboard(request: Request):
    try:
        project_data = json.load(open("data/mock_project_meta.json"))
    except Exception:
        project_data = []

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": project_data,
        "role": "ds"
    })