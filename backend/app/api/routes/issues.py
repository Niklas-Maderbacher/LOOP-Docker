from fastapi import APIRouter, HTTPException, Depends
from app.crud.issue import update_story_point
from app.api.schemas.issue import StoryPointUpdate 

router = APIRouter(prefix="/issues", tags=["issues"])

@router.patch("/{issue_id}")
async def update_issue_story_points(issue_id: int, update_data: StoryPointUpdate):
    if update_data.new_story_point_value  < 0:
        raise HTTPException(status_code=400, detail="Story points need to be positive integer values.")

    updated_issue = update_story_point(issue_id, update_data.new_story_point_value)

    if not updated_issue:
        raise HTTPException(status_code=204)

    return updated_issue

