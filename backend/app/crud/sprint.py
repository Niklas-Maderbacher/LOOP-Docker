from sqlmodel import Session
from app.db.models import Sprint

# LOOP-124
def get_sprints(db: Session, skip: int = 0, limit: int = 50) -> list[Sprint]:
    return db.query(Sprint).offset(skip).limit(limit).all()
