from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel, Field
from app.api.routes import FastApiAuthorization
from app.crud import project

from typing import List

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


# test model
class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    start_date: str | None = None
    end_date: str | None = None
    archived_at: str | None = None
    github_token: str | None = None

project_list: List[Project] = []

# returns all projects
@router.get("/get_all_projects")
async def get_all_projects():
    return {"projects": project_list}

# creates a new project using project model
# requires admin account
@router.post("/create_project", dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_project(project: Project):
    project_list.append(project)
    return HTTPException(status_code=201, detail="Project created")

# unarchives an archived project
# requires admin account
@router.post("/unarchive_project/{project_id}", dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_project(project_id: int):
    result = project.unarchive_project(project_id)

    if result is None:
        raise HTTPException(status_code=400, detail="Could not unarchive project")
    
    return HTTPException(status_code=201, detail=result)

