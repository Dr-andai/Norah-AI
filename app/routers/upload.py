from fastapi import APIRouter, UploadFle, File
from fastapi.responses import HTMLResponse
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/files", response_class=HTMLResponse)
async def upload_files(
    notebook: UploadFle = File(...),
    protocol: UploadFle = File(...),
    sop: UploadFle = File(...)
):
    uploads = {
        "notebook":notebook,
        "protocol":protocol,
        "sop":sop
    }

    for label, file in uploads.items():
        file_path = os.path.join(UPLOAD_DIR, f"{label}_{file.filename}")
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    return "<p>✅ Files uploaded successfully. You can now run Norah's analysis.</p>"