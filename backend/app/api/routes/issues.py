from fastapi import APIRouter, HTTPException, Depends, Response
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate, IssueUpdate
from app.api.deps import SessionDep
from app.crud.issue import get_issue, get_issues, update_issue, create_issue
from app.api.schemas.issue import IssueCreate
from app.db.models import Issue

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    """api call to update the story_points of an issue

    Args:
        issue_id (int): the id of the issue
        update_data (StoryPointUpdate): the new value of the story points

    Raises:
        HTTPException: 400 gets raised if the story points are negativ

    Returns:
        Issue: the updated issue 
    """
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue
