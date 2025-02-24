from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.schemas import IssueUpdatePriority
from app.models import Issue, User, Priority
from app.crud import update_priority

router = APIRouter()

@router.post("/update-priority/")
def update_issue_priority(issue_id: int, user_id: int, priority_name: str, db: Session = Depends(get_db)):
    """
    Updates the priority of an issue by creating a new entry with updated priority_id, version, updated_at, and updater_id.
    """
    # Check if issue exists
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if priority exists
    priority = db.query(Priority).filter(Priority.name == priority_name).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    
    # Call the CRUD function to create the new issue entry with updated priority
    new_issue = update_priority(db, issue, user_id, priority.id)
    
    if not new_issue:
        raise HTTPException(status_code=400, detail="Failed to update priority")
    
    return new_issue
