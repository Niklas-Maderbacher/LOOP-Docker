from sqlmodel import Session
from app.db.models import Attachment
from app.api.schemas.attachment import AttachmentCreate

def save_attachment(db: Session, attachment_data: AttachmentCreate) -> Attachment:
    """Saves the uploaded file attachment details in the database."""
    db_attachment = Attachment(
        issue_id=attachment_data.issue_id,
        link=attachment_data.link
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment
