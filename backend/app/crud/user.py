import uuid
from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import User, UserAtProject
from app.security.security import get_password_hash
from app.api.schemas.user import UserCreate

def get_project_role(db: Session, user_id, project_id):
    user = db.query(User).filter(User.id == user_id).first()
    
    # If the user is not found, you should return None or raise an exception
    if not user:
        print("No user found")
        return None  # or raise some custom exception

    # Now, get the role of the user for the specific project
    role = db.query(UserAtProject).filter(
        UserAtProject.project_id == project_id,
        UserAtProject.user_id == user.id
    ).first()  # We assume there is only one role per user per project

    return role.role if role else None

def add_admin_user(db: Session):
    new_user = User(
        email="admin@example.com",
        display_name="Admin User",
        password=get_password_hash("secret"),  # Make sure to hash the password
        is_admin=True,
        is_email_verified=True
    )
    db.add(new_user)
    db.commit()

def get_user(db: Session, email: str):
    """gets a user form the database by email

    Args:
        email (str): the email of the user

    Returns:
        User: the fetched user
    """
    user = db.query(User).filter(User.email == email).first()
    if user == None:
        return None 
    return user

def get_all_users(db: Session):
    """gets all users form the database

    Returns:
        List[User]: the list of users
    """
    users = db.query(User).all()
    return users


def create_user(db: Session, user: UserCreate):
    """creates a new user and saves it into the database

    Args:
        user (UserCreate): the data to create the user with

    Returns:
        User: the created user
    """
    new_user = User(
        email=user.email,
        display_name=user.display_name,
        password=get_password_hash(user.password),  # Make sure to hash the password
        microsoft_account=user.microsoft_account,
        archived = user.archived,
        last_active = user.last_active,
        is_email_verified = user.is_email_verified,
        mobile_number = user.mobile_number,
        is_admin=user.is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

