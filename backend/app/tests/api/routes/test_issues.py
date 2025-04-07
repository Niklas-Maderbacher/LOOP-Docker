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
    Updates the priority of an issue.

    - **issue_id**: ID of the issue whose priority needs to be updated.
    - **user_id**: ID of the user performing the change.
    - **priority_name**: The new priority name.
    - **session**: SQLAlchemy session for database interaction.

    **Responses:**
    - Returns the updated issue if the priority is successfully changed.
    - If an error occurs, an HTTPException is raised with the error detail.
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
    Updates the story points for an issue.

    - **issue_id**: ID of the issue whose story points need to be updated.
    - **update_data**: The new story points to be set.
    - **session**: SQLAlchemy session for database interaction.

    **Responses:**
    - Returns the updated issue if the story points are successfully changed.
    - If the new story points are invalid (e.g., negative), an HTTPException with the error detail is raised.
    - Returns a 204 response if no changes are required.
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
    """
    Helper function to update the priority of an issue.

    - **session**: SQLAlchemy session for database interaction.
    - **issue_id**: ID of the issue whose priority needs to be updated.
    - **user_id**: ID of the user performing the change.
    - **new_priority_name**: The new priority name.

    **Responses:**
    - Returns the updated issue if the priority is successfully changed.
    - If an error occurs (e.g., issue or priority does not exist), a ValueError is raised.
    """
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise ValueError(f"Issue with ID {issue_id} does not exist.")

    if not isinstance(new_priority_name, str):
        raise ValueError("Priority must be a string.")

    priority = session.query(Priority).filter(Priority.name == new_priority_name).first()
    if not priority:
        raise ValueError(f"Priority '{new_priority_name}' does not exist.")

    issue.priority_id = priority.id
    session.commit()
    session.refresh(issue)
    return issue
