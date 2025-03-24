from fastapi import APIRouter, HTTPException, Depends, Response
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate 
from app.api.deps import SessionDep
from app.crud.issue import get_issues
from app.api.schemas import IssueGet

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.get("/issues/", response_model=list[IssueGet])
async def read_issues(session: SessionDep):
    return get_issues(session)

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue
