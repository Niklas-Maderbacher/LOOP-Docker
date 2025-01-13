from fastapi import APIRouter

# routes imports go here
from app.api.routes import TEMPLATE_SHOWCASE
from app.api.routes import health_check

api_router = APIRouter()
api_router.include_router(TEMPLATE_SHOWCASE.router)
api_router.include_router(health_check.router)
# add more routers here:
# api_router.include_router(IMPORTED_ROUTER.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
