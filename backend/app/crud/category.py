from sqlmodel import Session
from app.db.models import Category

# LOOP-124
def get_categories(db: Session, skip: int = 0, limit: int = 50) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()
