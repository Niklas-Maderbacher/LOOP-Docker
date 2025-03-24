import uuid
from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import User, UserAtProject

def get_project_role(id, project_id):
    with next(get_db()) as db:
        # First, get the user based on email
        user = db.query(User).filter(User.id == id).first()
        
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

def add_admin_user():
    with next(get_db()) as db:
        new_user = User(
            email="admin@example.com",
            display_name="Admin User",
            password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # Make sure to hash the password
            is_admin=True,
            is_email_verified=True
        )
        db.add(new_user)
        db.commit()

# gets user from database To-Do
def get_user(email: str):
    with next(get_db()) as db:
        user = db.query(User).filter(User.email == email).first()
    return user

