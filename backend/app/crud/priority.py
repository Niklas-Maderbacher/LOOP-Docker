from app.db.models import Priority, Issue, User
from sqlmodel import Session
from app.enums.priority import Priority


# LOOP-124
def get_priorities():
    return [Priority.HIGH, Priority.LOW, Priority.MEDIUM, Priority.VHIGH, Priority.VLOW]


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

