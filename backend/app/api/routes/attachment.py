import requests
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session
from app.crud.attachment import save_attachment
from app.api.schemas.attachment import AttachmentCreate
from app.api.deps import SessionDep

router = APIRouter(prefix="/attachments", tags=["Attachments"])

IMAGE_SERVER_URL = "http://image-server.com/upload"  # Ändere diese URL auf deinen Image-Server

@router.post("/")
async def upload_file(
    session: SessionDep, 
    issue_id: int, 
    file: UploadFile = File(...)
):
    """Empfängt eine Datei, sendet sie an den Image-Server und speichert den zurückgegebenen Pfad."""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="Keine Datei übermittelt.")

    files = {"file": (file.filename, file.file, file.content_type)}

    # Datei an den externen Image-Server senden
    response = requests.post(IMAGE_SERVER_URL, files=files)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Fehler beim Hochladen zum Image-Server")

    image_server_data = response.json()
    file_path = image_server_data.get("file_path")  # Erwartet: Der Server gibt den Dateipfad zurück

    if not file_path:
        raise HTTPException(status_code=500, detail="Kein Dateipfad vom Image-Server erhalten.")

    # Datei-Referenz in der Datenbank speichern
    attachment_data = AttachmentCreate(issue_id=issue_id, link=file_path)
    saved_attachment = save_attachment(session, attachment_data)

    return {
        "message": "Datei erfolgreich hochgeladen",
        "attachment": saved_attachment,
        "file_path": file_path
    }
