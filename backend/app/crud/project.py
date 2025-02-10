from typing import List
from typing import Optional
from datetime import datetime
from sqlmodel import Session
from app.db.models import Project
from app.api.schemas.project import ProjectCreate

def get_all_projects(db: Session, skip: int = 0, limit: int = 50) -> List[Project]:
    """Returns all projects from the database.

    Args:
        db (Session): Database session
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 50.

    Returns:
        List[Project]: List of Project objects
    """
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    """Creates a new project in the database.

    Args:
        db (Session): Database session
        project (Project): Project instance to create

    Returns:
        Project: The created project instance
    """
    db_project = Project(
        name=project.name,
        start_date=project.start_date,
        github_token=project.github_token
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def is_not_archived(project: Project) -> bool:
    """Checks if a project is not archived based on the archived_at field."""
    return project.archived_at is None

def archive_project(db: Session, project_id: int) -> Optional[Project]:
    """Archives a project by setting the archived_at column to the current date."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None

    if not is_not_archived(db_project):
        return "already_archived"

    db_project.archived_at = datetime.utcnow().isoformat()  # Set current UTC datetime
    db.commit()
    db.refresh(db_project)
    return db_project
