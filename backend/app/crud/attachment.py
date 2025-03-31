from sqlmodel import Session
from app.db.models import Attachment
from app.api.schemas.attachment import AttachmentCreate
from app.db.models import Issue

def save_attachment(db: Session, attachment_data: AttachmentCreate) -> Attachment:
    """
    Saves project_id, issue_id, and the filename in the database.

    Args:
        db (Session): The database session.
        attachment_data (AttachmentCreate): Data transfer object containing the issue ID, 
                                            project ID, and filename.

    Returns:
        Attachment: The newly created Attachment object.
    """
    db_attachment = Attachment(
        issue_id=attachment_data.issue_id,
        project_id=attachment_data.project_id,
        filename=attachment_data.filename,
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def delete_attachment_by_details(db: Session, project_id: int, issue_id: int, filename: str) -> bool:
    """
    Deletes an attachment from the database that matches the specified project_id, 
    issue_id, and filename.

    Args:
        db (Session): The database session.
        project_id (int): The ID of the project.
        issue_id (int): The ID of the issue.
        filename (str): The filename (as provided by the file server).

    Returns:
        bool: True if the attachment was found and deleted, False if no such 
              attachment existed.
    """
    issue = db.get(Issue, issue_id)
    if not issue:
        return False

    db_attachment = (
        db.query(Attachment)
        .filter(Attachment.project_id == issue.project_id)
        .filter(Attachment.issue_id == issue_id)
        .filter(Attachment.filename == filename)
        .first()
    )

    if not db_attachment:
        return False

    db.delete(db_attachment)
    db.commit()
    return True
