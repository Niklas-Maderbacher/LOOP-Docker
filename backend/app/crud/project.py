from typing import List
from sqlmodel import Session, select
from app.db.models import Project

def get_all_projects(db: Session, skip: int = 0, limit: int = 50) -> List[Project]:
    """function returns all projects from db

    Args:
        db (Session): database session
        skip (int, optional): how many values should be skipped before returning values (paging). Defaults to 0.
        limit (int, optional): how many values should be returned at max. Defaults to 50.

    Returns:
        List[Project]: List of projects found in the db of type Project.
    """
    statement = select(Project).offset(skip).limit(limit)
    projects = db.exec(statement).all()
    return projects

def create_project(db: Session, project: Project) -> Project:
    """functions creates a new db entry of type Project

    Args:
        db (Session): db session
        project (Project): the project object that should be inserted

    Returns:
        Project: the project object that got inserted
    """
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
