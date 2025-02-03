from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.api.routes import FastApiAuthorization
import app.crud.project as crud_project; 
from app.api.deps import SessionDep

from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

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

# update user role
@router.patch("/{project_id}/users/{user_id}/role")
async def update_user_role(session: SessionDep, project_id: int, user_id: int, new_role_id: int):
    if crud_project.update_user_role(session, project_id, user_id, new_role_id) == None:
        return HTTPException(status_code=500)
    else:
        return HTTPException(status_code=200)