from fastapi import APIRouter
from app.api.deps import SessionDep
from app.crud.priority import get_priorities

router = APIRouter(prefix="/priorities", tags=["Sprints"])

# LOOP-124
@router.get("/")
async def get_priorities_api(session: SessionDep):
    """api call to get all priorities from the database

    Returns:
        List[Priority]: the list of priorities
    """
    return get_priorities()
