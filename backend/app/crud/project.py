from typing import List

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
