from fastapi import APIRouter, HTTPException, Depends, Response
from app.crud.priority import update_priority
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate
from app.api.deps import SessionDep
from sqlalchemy.orm import Session

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/update-priority")
def update_issue_priority(
    issue_id: int,
    user_id: int,
    priority_name: str,
    session: Session = Depends(SessionDep)
):
    """
    Aktualisiert die Priorität eines Issues.
    """
    try:
        updated_issue = update_priority(session, issue_id, user_id, priority_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated_issue:
        raise HTTPException(status_code=400, detail="Failed to update priority")

    return updated_issue


@router.patch("/{issue_id}")
async def update_issue_story_points(
    session: SessionDep,
    issue_id: int,
    update_data: StoryPointUpdate
):
    """
    Aktualisiert Story Points für ein Issue.
    """
    if update_data.new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    try:
        updated_issue = update_story_point(session, issue_id, update_data.new_story_point_value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_issue is None:
        return Response(status_code=204)

    return updated_issue

def update_priority(session: Session, issue_id: int, user_id: int, new_priority_name: str):
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise ValueError(f"Issue mit ID {issue_id} existiert nicht.")

    if not isinstance(new_priority_name, str):
        raise ValueError("Priority muss ein String sein.")

    priority = session.query(Priority).filter(Priority.name == new_priority_name).first()
    if not priority:
        raise ValueError(f"Priority '{new_priority_name}' existiert nicht.")

    issue.priority_id = priority.id
    session.commit()
    session.refresh(issue)
    return issue

