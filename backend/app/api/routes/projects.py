from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.api.routes import FastApiAuthorization

from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    start_date: str | None = None
    end_date: str | None = None
    archived_at: str | None = None
    github_token: str | None = None

project_list: List[Project] = []

@router.get("/get_all_projects")
async def get_all_projects():
    return {"projects": project_list}


@router.post("/create_project", dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_project(project: Project):
    project_list.append(project)
    return HTTPException(status_code=201, detail="Project created")
