from fastapi import APIRouter
from app.api.deps import SessionDep
from app.crud.sprint import get_sprints

router = APIRouter(prefix="/sprints", tags=["Sprints"])

# LOOP-124
@router.get("/")
async def get_sprints_api(session: SessionDep):
    """api call to get all sprints from the database

    Returns:
        List[Category]: the list of sprints
    """
    return get_sprints(session)