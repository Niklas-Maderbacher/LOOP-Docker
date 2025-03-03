from fastapi import APIRouter, HTTPException, Depends
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate, IssueCreate, IssueUpdate, IssueResponse
from app.api.deps import SessionDep
import app.crud.issue as crud_issue
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/issues", tags=["Issues"])

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    if update_data.new_story_point_value  < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if not updated_issue:
        raise HTTPException(status_code=204)

    return updated_issue

@router.post("/create-issue")
async def create_issue(session: SessionDep, issue_data: IssueCreate):
    issue = crud_issue.create_issue(session, issue_data)

    return issue

@router.put("/update-issue/{issue_id}")
async def create_issue(session: SessionDep, issue_id: int, issue_data: IssueUpdate):
    crud_issue.update_issue(session, issue_id, issue_data)