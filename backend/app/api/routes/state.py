from fastapi import APIRouter
from app.api.deps import SessionDep
from app.crud.state import get_states 

router = APIRouter(prefix="/states", tags=["States"])

# LOOP-124
@router.get("/")
async def get_states_api(session: SessionDep):
    """api call to get all states from the database

    Returns:
        List[State]: the list of states
    """
    return get_states(session)
