from fastapi import APIRouter

# routes imports go here
from app.api.routes import TEMPLATE_SHOWCASE

api_router = APIRouter()
api_router.include_router(TEMPLATE_SHOWCASE.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
