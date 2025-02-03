from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import User, Project
from datetime import datetime

def unarchive_project(user_id, project_id):
    with next(get_db()) as db:
        # Get the user by id and check if it is an admin
        user = db.query(User).filter(User.id == user_id, User.is_admin == True).first()

        # If no user is found or user is not an admin
        if not user:
            return None # Or raise custom exception
        
        # Get project based on the id
        project = db.query(Project).filter(Project.id == project_id).first()

        # If no project is found
        if not project:
            return None # Or raise custom exception
        
        # If project is not archived
        if not project.archived_at:
            return None # Or raise custom exception
        
        project.archived_at = None
        db.add(project)
        db.commit()
        db.refresh(project)

        return {"message": "Project unarchived successfully", "project_id": project.id}