from app.db.models import Priority, Issue, User
from sqlmodel import Session


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

    new_issue = Issue(
        id=issue.id,
        id=issue.id,
        name=issue.name,
        category_id=issue.category_id,
        sprint_id=issue.sprint_id,
        state_id=issue.state_id,
        creator_id=issue.creator_id,
        responsible_user_id=issue.responsible_user_id,
        priority_id=issue.priority_id,
        description=issue.description,
        repository_link=issue.repository_link,
        story_points=issue.story_points,
        report_time=issue.report_time,
        version=issue.version,
        updater_id=issue.updater_id,
        project_id=issue.project_id,
        updated_at=issue.updated_at,
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
