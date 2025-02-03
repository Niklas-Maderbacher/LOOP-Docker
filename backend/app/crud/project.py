from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import User, Project
from datetime import datetime

def unarchive_project(project_id):
    with next(get_db()) as db:
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