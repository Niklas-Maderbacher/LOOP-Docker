from typing import List

from sqlalchemy.orm import Session
from app.db.models import User

def get_all_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, display_name: str, skip: int = 0, limit: int = 50) -> List[User]:
    return db.query(User).offset(skip).limit(limit).filter(User.display_name == display_name).all()

def create_user(db: Session, user: User) -> User:
  db_user = User(**user.model_dump())
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user
