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


@router.post("/sign_up", status_code=201)
async def sign_up_user(session: SessionDep, user: UserCreate):
    """Public api call to create a new user account (sign-up)

    Args:
        user (UserCreate): the schema for creating a user (the data)

    Raises:
        HTTPException: 400 if the user with that email already exists

    Returns:
        dict: success message with user info
    """
    try:
        existing_user = crud.get_user(session, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists.")
        
        sign_up_data = UserCreate(
            email=user.email,
            display_name=user.display_name,
            password=user.password,
            microsoft_account=getattr(user, 'microsoft_account', None),
            archived="False",  
            last_active=None,  
            is_email_verified=False,  
            mobile_number=getattr(user, 'mobile_number', None),
            is_admin=False  
        )
        
        created_user = crud.create_user(session, sign_up_data)
        
        return {
            "message": "Account created successfully",
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "display_name": created_user.display_name
            }
        }
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists.")