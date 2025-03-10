from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session
import shutil
import os
from app.crud.attachment import save_attachment
from app.api.schemas.attachment import AttachmentCreate
from app.api.deps import SessionDep

router = APIRouter(prefix="/attachments", tags=["Attachments"])

UPLOAD_DIR = "uploads"  # Directory where files will be stored
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

@router.post("/")
async def upload_file(session: SessionDep, issue_id: int, file: UploadFile = File(...)):
    """Handles file uploads and saves them as issue attachments."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save attachment info in the database
    attachment_data = AttachmentCreate(issue_id=issue_id, link=file_path)
    saved_attachment = save_attachment(session, attachment_data)

    return {"message": "File uploaded successfully", "attachment": saved_attachment}
