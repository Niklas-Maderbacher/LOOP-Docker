from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=str, status_code=200)
def get_template():
    return "test"
