from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel, Field
from app.api.routes import FastApiAuthorization
from app.crud import project

from typing import List
from typing import Optional
from datetime import datetime
from app.api.routes import FastApiAuthorization
from app.api.deps import SessionDep
from app.db.models import Project
import app.crud.project as crud_project
from app.api.schemas.project import ProjectCreate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[Project], status_code=200)
async def get_all_projects(session: SessionDep):
    """returns all projects in db

    Args:
        session (SessionDep): db session

    Returns:
        list: list of all projects in the db
    """
    return list(crud_project.get_all_projects(session))

@router.post("/", response_model=Project, dependencies=[Depends(FastApiAuthorization.is_admin)], status_code=201)
async def create_project(session: SessionDep, project: ProjectCreate):
    """adds a new project to the db based on the Project model, requires admin permissions

    Args:
        session (SessionDep): db session
        project (Project): project to be inserted of type Project

    Raises:
        HTTPException: 400 on fail, 201 on success

    Returns:
        HTTPException: status code 201 (success)
    """
    db_project = crud_project.create_project(session, project)
    if not db_project:
        raise HTTPException(status_code=400, detail="Failed to create project")
    return db_project

@router.put("/unarchive-project/{project_id}", dependencies=[Depends(FastApiAuthorization.is_admin)], status_code=201)
async def unarchive_project(session: SessionDep, project_id: int):
    """unarchives a specific project in the database, requires admin permission

    Args:
        session (SessionDep): db session
        project_id (int): the id of the project to unarchive

    Raises:
        HTTPException: 400 on fail, 201 on success

    Returns:
        HTTPException: status code 201 (success)
    """
    result = project.unarchive_project(session, project_id)

    if result is None:
        raise HTTPException(status_code=400, detail="Could not unarchive project")
    
    return result


@router.put("/{project_id}/users/{user_id}/role", status_code=200)
async def update_user_role(session: SessionDep, project_id: int, user_id: int, new_role_id: int):
    """
    updates user role

    Args:
        session (SessionDep): db session
        project_id (int): Id of the project
        user_id (int): Id of the user
        new_role_id (int): Id of the new user role

    Raises:
        HTTPException: 400 on fail

    Returns:
        UserAtProject: updated UserAtProject object
    """
    project_user_role = crud_project.update_user_role(session, project_id, user_id, new_role_id)
    if not project_user_role:
        raise HTTPException(status_code=400, detail="can not update user role")
    return project_user_role

@router.put("/{project_id}/archive", response_model=Optional[Project], dependencies=[Depends(FastApiAuthorization.is_admin)], status_code=200)
async def archive_project(session: SessionDep, project_id: int):
    """Archives a project by setting its archived_at field to the current date."""
    db_project = session.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not crud_project.is_not_archived(db_project):
        raise HTTPException(status_code=400, detail="Project is already archived")

    updated_project = crud_project.archive_project(session, project_id)
    
    if updated_project == "already_archived":
        raise HTTPException(status_code=400, detail="Project is already archived")
    
    return updated_project

