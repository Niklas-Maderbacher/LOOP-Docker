from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import app.crud.user as crud
from app.api.routes import FastApiAuthorization
from app.api.deps import SessionDep
from sqlalchemy.exc import IntegrityError
from app.db.models import User
from app.api.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

# legacy

# test model
class User(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    is_admin: bool = Field(...)
    microsoft_account: bool | None = None
    archived: str | None = None
    last_active: str | None = None
    is_email_verified: bool | None = None
    mobile_number: str | None = None

user_list: List[User] = []

# LOOP-124
@router.get("/get_all_users")
async def get_all_users(session: SessionDep):
    """api call to get all users

    Returns:
        List[User]: list of all users 
    """
    return crud.get_all_users(session)

@router.get("/get_user/{email}")
async def get_user(session: SessionDep, email: str):
    """api call to get a specific user by email

    Raises:
        HTTPException: 404 if the user doesn't exist

    Returns:
        User: the user
    """
    user = crud.get_user(session, email)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create_user", dependencies=[Depends(FastApiAuthorization.is_admin)], status_code=201)
async def register_user(session: SessionDep, user: UserCreate):
    """api call to create a user

    Args:
        user (UserCreate): the schema for creating a user (the data)

    Raises:
        HTTPException: 404 if the user with that email already exists

    Returns:
        User: the created user 
    """
    try:
        created_user = crud.create_user(session, user)
        return created_user
    except IntegrityError:
        raise HTTPException(status_code=404, detail=f"User with email {user.email} already exist.")

# path call to return user with specified name
@router.get("/get_user/{display_name}")
async def get_user(display_name: str):
    for user in user_list:
        if user.display_name == display_name:
            return {"item": user}
    raise HTTPException(status_code=404, detail="User not found")

# creates a new user with model
# requires admin account
@router.post("/create_user", dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_user(user: User):
    user_list.append(user)
    return HTTPException(status_code=201, detail="User created")

