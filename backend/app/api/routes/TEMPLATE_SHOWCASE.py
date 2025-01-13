from fastapi import APIRouter

router = APIRouter(prefix="/showcase", tags=["showcase"])


@router.get("/", response_model=str, status_code=200)
def get_template():
    return "test"
