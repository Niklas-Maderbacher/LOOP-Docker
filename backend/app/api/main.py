from fastapi import APIRouter

# routes imports go here
from app.api.routes import TEMPLATE_SHOWCASE
from app.api.routes import health_check
from app.api.routes import FastApiAuthorization
from app.api.routes import projects
from app.api.routes import users
from app.api.routes import issue

api_router = APIRouter()
api_router.include_router(TEMPLATE_SHOWCASE.router)
api_router.include_router(health_check.router)
# api_router.include_router(users.router) TODO
api_router.include_router(projects.router)
api_router.include_router(issue.router)
api_router.include_router(FastApiAuthorization.router)
api_router.include_router(issues.router)
# add more routers here:
# api_router.include_router(IMPORTED_ROUTER.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
