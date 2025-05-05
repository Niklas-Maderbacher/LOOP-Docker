from fastapi import APIRouter
from app.api.deps import SessionDep
from app.crud.category import get_categories   

router = APIRouter(prefix="/categories", tags=["Categories"])

# LOOP-124
@router.get("/")
async def get_categories_api(session: SessionDep):
    """api call to get all categories from the database

    Returns:
        List[Category]: the list of categories
    """
    return get_categories(session)