import os
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlmodel import Session

from app.crud.attachment import save_attachment, delete_attachment_by_details
from app.api.schemas.attachment import AttachmentCreate
from app.api.deps import SessionDep

router = APIRouter(prefix="/attachments", tags=["Attachments"])

# Load image-server configuration from .env
load_dotenv()
IMAGE_SERVER_URL = os.getenv("FILE_SERVER_IP")
IMAGE_SERVER_PORT = os.getenv("FILE_SERVER_PORT")

# Validate environment variables (must not be empty)
if not IMAGE_SERVER_URL or not IMAGE_SERVER_PORT:
    raise ValueError("FILE_SERVER_IP oder FILE_SERVER_PORT nicht in der .env Datei gesetzt")

# Define endpoints for upload and delete on the file server
IMAGE_SERVER_UPLOAD_ENDPOINT = f"http://{IMAGE_SERVER_URL}:{IMAGE_SERVER_PORT}/dump"
IMAGE_SERVER_DELETE_ENDPOINT = f"http://{IMAGE_SERVER_URL}:{IMAGE_SERVER_PORT}/attachments"

@router.post("/")
async def upload_files(
    session: SessionDep,
    project_id: int = Form(...),
    issue_id: int = Form(...),
    files: list[UploadFile] = File(...),
):
    """
    Receives multiple files from the frontend in one request,
    but for each individual file, it sends a separate POST request to the file server.
    After successfully uploading each file, the filename is saved to the database.
    """

    # If no files are provided, raise an error
    if not files:
        raise HTTPException(status_code=400, detail="Keine Dateien übermittelt.")

    uploaded_attachments = []

    # Iterate over each file, sending a single request per file to the file server
    for single_file in files:
        file_data = [
            ("file", (single_file.filename, single_file.file, single_file.content_type))
        ]
        metadata = {
            "project_id": str(project_id),
            "issue_id": str(issue_id)
        }

        # Perform a POST request to the file server for this single file
        response = requests.post(IMAGE_SERVER_UPLOAD_ENDPOINT, files=file_data, data=metadata)

        # If the file server doesn't return a 201 status
        if response.status_code != 201:
            raise HTTPException(
                status_code=500,
                detail=f"Fehler beim Hochladen zum File-Server, Status: {response.status_code}"
            )

        server_response = response.json()
        filename_from_server = server_response.get("filename")
        if not filename_from_server:
            raise HTTPException(status_code=500, detail="Kein 'filename' vom Image-Server erhalten.")

        attachment_data = AttachmentCreate(
            issue_id=issue_id,
            project_id=project_id,
            filename=filename_from_server
        )
        saved_attachment = save_attachment(session, attachment_data)

        uploaded_attachments.append({
            "attachment_id": saved_attachment.id,
            "filename": saved_attachment.filename
        })

    return {
        "message": "Alle Dateien erfolgreich hochgeladen",
        "project_id": project_id,
        "issue_id": issue_id,
        "uploaded_attachments": uploaded_attachments
    }


@router.delete("/{project_id}/{issue_id}/{filename}", status_code=204)
async def delete_file_from_backend(
    project_id: int,
    issue_id: int,
    filename: str,
    session: SessionDep
):
    """
    1) Calls the file server to delete the specified attachment.
    2) If successful, also deletes the attachment record from the database.
    3) Returns a 204 (No Content) status if everything goes well.
    """
    response = requests.delete(IMAGE_SERVER_DELETE_ENDPOINT + f"/{project_id}/{issue_id}/{filename}")
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"File-Server konnte Datei nicht löschen (Status: {response.status_code})"
        )

    # If deletion on the file server was successful, remove the database record
    success = delete_attachment_by_details(session, project_id, issue_id, filename)
    if not success:
        raise HTTPException(status_code=404, detail="Attachment nicht in der DB gefunden.")

    return
