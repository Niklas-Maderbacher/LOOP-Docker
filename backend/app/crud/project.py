from typing import List
from typing import Optional
from datetime import datetime
from sqlmodel import Session
from app.db.models import Project
from app.api.schemas.project import ProjectCreate
from app.db.models import UserAtProject, User
from app.enums.role import Role

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
        key=project.key,
        start_date=project.start_date,
        end_date=project.end_date,
        github_token=project.github_token
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project



def unarchive_project(db: Session, project_id: int):
    """Unarchives a project in the database

    Args:
        db (Session): Database session
        project_id (int): Id of the project to unarchive

    Returns:
        Project: The updated project instance
        None: When no project is found or project is not archived
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        return None
    
    if not db_project.archived_at:
        return None
    
    db_project.archived_at = None
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def update_user_role(db: Session, project_id: int, user_id: int, new_role: Role):
    """
    updates a user's role within a project
    checks whether the specified new role and user exist

    Args:
        db (Session): Database session
        project_id (int): Id of the projekt
        user_id (int): Id of the user
        new_role_id (int): Id of the new user role

    Returns:
        useratproject | none: returns the updated UserAtProject object if the update was successful, otherwise none
    """
    
    if not db.query(User).filter(User.id == user_id).first():
        return None

    user_at_project = db.query(UserAtProject).filter(
        UserAtProject.project_id == project_id,
        UserAtProject.user_id == user_id
    ).first()

    if not user_at_project:
        return None

    user_at_project.role = new_role
    db.commit()
    db.refresh(user_at_project)

    return user_at_project

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

