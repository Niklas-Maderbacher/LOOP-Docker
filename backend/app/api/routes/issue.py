from fastapi import APIRouter, HTTPException, Depends, Response
from app.api.deps import SessionDep
from app.crud.issue import update_story_point, create_issue
from app.api.schemas.issue import StoryPointUpdate, IssueCreate
from app.db.models import Issue
from app.crud.priority import update_priority

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/update-priority")
def update_issue_priority(session: SessionDep, issue_id: int, user_id: int, priority_name: str):
    updated_issue = update_priority(session, issue_id, user_id, priority_name)

    if not updated_issue:
        raise HTTPException(status_code=400, detail="Failed to update priority")

    return updated_issue

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    """
    Aktualisiert die Story Points eines Issues.
    
    Args:
        session: Datenbanksitzung
        issue_id: ID des zu aktualisierenden Issues
        update_data: Die neuen Story-Point-Daten
        
    Returns:
        Das aktualisierte Issue oder einen 204-Status, wenn das Issue nicht gefunden wurde
    """
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue

@router.post("/create", response_model=Issue, status_code=201)
async def create_new_issue(session: SessionDep, issue_data: IssueCreate):
    """
    Erstellt ein neues Issue in der Datenbank.

    Args:
        session: Datenbanksitzung
        issue_data: Issue-Daten

    Returns:
        Issue: Das erstellte Issue-Objekt
    """
    if not issue_data.name or not issue_data.description:
        raise HTTPException(status_code=400, detail="Name and description are required fields.")

    if issue_data.story_points is not None and issue_data.story_points < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")
        
    new_issue = create_issue(session, issue_data)

    if not new_issue:
        raise HTTPException(status_code=400, detail="Failed to create issue.")
    
    return new_issue