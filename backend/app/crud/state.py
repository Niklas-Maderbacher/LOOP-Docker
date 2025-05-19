from sqlmodel import Session
from app.db.models import State

# LOOP-124
def get_states(db: Session, skip: int = 0, limit: int = 50) -> list[State]:
    return db.query(State).offset(skip).limit(limit).all()
