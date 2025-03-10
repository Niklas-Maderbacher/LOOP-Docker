from app.db.models import Issue, Priority, User
from sqlmodel import Session
from datetime import datetime
from app.api.deps import get_db  # Funktion, um die DB-Session zu erhalten

def update_priority(issue_id: int, user_id: int, new_priority_name: str):
    # Holt die Sitzung aus der Datenbank
    session = next(get_db())  # Wir gehen davon aus, dass get_db() eine Generator-Funktion ist, die die Sitzung bereitstellt

    # Überprüfen, ob der User existiert
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User mit ID {user_id} existiert nicht.")
    
    # Überprüfen, ob das Issue existiert
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise ValueError(f"Issue mit ID {issue_id} existiert nicht.")
    
    if issue.version is None:
            issue.version = 0  # Falls die Version `None` ist, auf 0 setzen
    
    # Überprüfen, ob die Priority existiert
    priority = session.query(Priority).filter(Priority.name == new_priority_name).first()
    if not priority:
        raise ValueError(f"Priority '{new_priority_name}' existiert nicht.")
    
    # Erstellen eines neuen Issue-Eintrags mit aktualisierter Priorität
    new_issue = Issue(
        name=issue.name,
        category_id=issue.category_id,
        sprint_id=issue.sprint_id,
        state_id=issue.state_id,
        creator_id=issue.creator_id,
        responsible_user_id=issue.responsible_user_id,
        priority_id=priority.id,
        description=issue.description,
        repository_link=issue.repository_link,
        story_points=issue.story_points,
        report_time=issue.report_time,
        version=issue.version + 1,
        updater_id=user.id,
        project_id=issue.project_id,
        updated_at=datetime.utcnow(),
        created_at=issue.created_at,
        backlog_order_number=issue.backlog_order_number,
        deleted_at=issue.deleted_at,
        finisher_id=issue.finisher_id,
        parent_issue_id=issue.parent_issue_id,
    )

    session.add(new_issue)
    session.commit()
    session.refresh(new_issue)

    return new_issue
