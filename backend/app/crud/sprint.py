from sqlmodel import Session
from app.db.models import Sprint

# LOOP-124
def get_sprints(db: Session, skip: int = 0, limit: int = 50) -> list[Sprint]:
    return db.query(Sprint).offset(skip).limit(limit).all()

# LOOP-124
def get_sprints_by_project(db: Session, project_id:int, skip: int = 0, limit: int = 50) -> list[Sprint]:
    return db.query(Sprint).filter(Sprint.project_id == project_id).offset(skip).limit(limit).all()
