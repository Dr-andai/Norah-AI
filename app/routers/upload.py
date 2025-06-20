from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
import os
import shutil

router = APIRouter()

UPLOAD_DIR = os.path.join("/data","uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/files", response_class=HTMLResponse)
async def upload_files(
    notebook: UploadFile = File(...),
    protocol: UploadFile = File(...),
    sop: UploadFile = File(...)
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