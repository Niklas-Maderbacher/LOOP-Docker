from app.db.models import Priority
from sqlmodel import Session


def set_priority_update(session: Session, issue_id: int, new_priority: str):
    
    statement = select(Priority).where(Priority.name == new_priority)
    priority = session.exec(statement).first()

    if not priority:
        raise ValueError(f"Priority '{new_priority}' nicht gefunden")

    statement = select(Issue).where(Issue.id == issue_id)
    issue = session.exec(statement).first()

    if not issue:
        raise ValueError(f"Issue mit ID {issue_id} nicht gefunden")

    issue.priority_id = priority.id
    session.add(issue)
    session.commit()
    session.refresh(issue)

    return issue  # Gibt das aktualisierte Issue zurück
