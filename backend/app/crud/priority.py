from app.db.models import Priority, Issue, User
from sqlmodel import Session

# LOOP-124
def get_priorities(db: Session, skip: int = 0, limit: int = 50) -> list[Priority]:
    return db.query(Priority).offset(skip).limit(limit).all()


def update_priority(session: Session, issue_id: int, user_id: int, new_priority: str):
    
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User mit ID {user_id} existiert nicht.")

    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise ValueError(f"Issue mit ID {issue_id} existiert nicht.")

    priority = session.query(Priority).filter(Priority.name == new_priority).first()
    if not priority:
        raise ValueError(f"Priority '{new_priority}' existiert nicht.")

    issue.priority_id = priority.id
    session.commit()
    session.refresh(issue)

    return issue  

