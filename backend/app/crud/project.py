from typing import List

from sqlmodel import Session
from app.db.models import Project
from app.api.schemas.project import ProjectCreate
from app.db.models import UserAtProject, Role, User

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


def update_user_role(db: Session, project_id: int, user_id: int, new_role_id: int):
    """_summary_

    Args:
        db (Session): Database session
        project_id (int): Id of the projekt
        user_id (int): Id of the user
        new_role_id (int): Id of the new user role

    Returns:
        useratproject: _description_
    """
    if not db.query(Role).filter(Role.id == new_role_id).first():
        return None
    
    if not db.query(User).filter(User.id == user_id).first():
        return None

    user_at_project = db.query(UserAtProject).filter(
        UserAtProject.project_id == project_id,
        UserAtProject.user_id == user_id
    ).first()

    if not user_at_project:
        return None

    user_at_project.role_id = new_role_id
    db.commit()
    db.refresh(user_at_project)

    return user_at_project
