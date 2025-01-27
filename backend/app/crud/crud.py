import uuid
from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import User

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
def get_user(user_email: str):
    with get_db() as db:
        user = db.exec(select(User).where(User.email == user_email))
    return user

# def get_project_role(user_email, project_id):
#     with get_db() as db:
#         user = db.exec(select(User).where(User.email == user_email)).first()
#         role = db.exec(select(UserAtProject).where(
#         (UserAtProject.project_id == project_id) & 
#         (UserAtProject.user_id == user.user_id)
#         ))

#     return role.role_id
