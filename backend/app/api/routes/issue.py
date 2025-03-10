from app.api.routes import FastApiAuthorization
from app.crud.priority import update_priority  
from fastapi import APIRouter, HTTPException, Depends, Response
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate 
from app.api.deps import SessionDep

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/update-priority")
def update_issue_priority(issue_id: int, user_id: int, priority_name: str):
    """
    Ruft die CRUD-Funktion auf, um die Priorität eines Issues in der Datenbank zu aktualisieren.
    """
    # Aufrufen der CRUD-Funktion zum Aktualisieren der Priorität des Issues
    updated_issue = update_priority(issue_id, user_id, priority_name)

    if not updated_issue:
        raise HTTPException(status_code=400, detail="Failed to update priority")

    return updated_issue

@router.patch("/{issue_id}")
async def update_issue_story_points(session: SessionDep, issue_id: int, update_data: StoryPointUpdate):
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue
