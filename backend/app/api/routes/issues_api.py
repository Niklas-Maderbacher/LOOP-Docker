from fastapi import APIRouter, HTTPException, Depends, Response, Query
from app.db.models import Issue
from app.crud.issues import update_story_point
from app.api.schemas.issue import StoryPointUpdate 
from app.api.deps import SessionDep
from app.crud.issues import get_issues, create_issue
from app.api.schemas.issue import GetIssue, IssueCreate
from app.db.models import Issue

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.get("/issues/", response_model=list[GetIssue])
async def read_issues(session: SessionDep):
    return get_issues(session)

@router.get("/issues/", response_model=list[GetIssue], status_code=200)
async def read_issues(project_id: int = Query(default=None), session: SessionDep = Depends()):
    if project_id is not None:
        return session.query(Issue).filter(Issue.project_id == project_id).all()
    return get_issues(session)

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue

@router.post("/create", response_model=Issue, status_code=201)
async def create_new_issue(session: SessionDep, issue_data: IssueCreate):
    """Creates a new issue in the database.

    Args:
        session (SessionDep): Database session
        issue_data (IssueCreate): Issue data

    Returns:
        Issue: Created issue object
    """
    if not issue_data.name or not issue_data.description:
        raise HTTPException(status_code=400, detail="Name and description are required fields.")

    new_issue = create_issue(session, issue_data)

    if not new_issue:
        raise HTTPException(status_code=400, detail="Failed to create issue.")

    if issue_data.story_points:
        if issue_data.story_points <= 0:
            raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")
    
    return new_issue
