from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.sprint import SprintCreate
from app.crud import sprint as crud_sprint
from app.api.deps import SessionDep
from sqlalchemy.exc import IntegrityError
from app.api.routes.FastApiAuthorization import get_current_user

## Loop-101 Thomas Sommerauer
router = APIRouter(prefix="/sprints", tags=["Sprints"])

@router.post("/create", status_code=201)
def create_sprint(
    sprint: SprintCreate,
    session: SessionDep,
    current_user=Depends(get_current_user)
):
    try:
        return crud_sprint.create_sprint(
            db=session,
            user_id=current_user.id,
            sprint_data=sprint
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Database error")
################################################