from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List

from app.api.routes import FastApiAuthorization
from app.api.deps import SessionDep
from app.db.models import Project
import app.crud.project as crud_project

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[Project])
async def get_all_projects(session: SessionDep):
    """returns all projects in db

    Args:
        session (SessionDep): db session

    Returns:
        list: list of all projects in the db
    """
    return list(crud_project.get_all_projects(session))

@router.post("/", response_model=Project, dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_project(session: SessionDep, project: Project):
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
    return HTTPException(status_code=201, detail="Project created")
