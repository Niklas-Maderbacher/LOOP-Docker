from fastapi import APIRouter
from app.api.deps import SessionDep
from app.crud.sprint import get_sprints, get_sprints_by_project

router = APIRouter(prefix="/sprints", tags=["Sprints"])

# LOOP-124
@router.get("/")
async def get_sprints_api(session: SessionDep):
    """api call to get all sprints from the database

    Returns:
        List[Category]: the list of sprints
    """
    return get_sprints(session)

# LOOP-124
@router.get("/project/{project_id}")
async def get_sprints_by_project_api(session: SessionDep, project_id:int):
    """api call to get all sprints from the database

    Returns:
        List[Category]: the list of sprints
    """
    return get_sprints_by_project(session, project_id)
