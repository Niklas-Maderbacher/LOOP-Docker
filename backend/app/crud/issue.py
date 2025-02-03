from app.db.models import Issue
from sqlmodel import Session, select


def create_issue(session: Session, user: Issue) -> Issue:
    issue_db = Issue(
        id=Issue.id,
        name=Issue.name,
        category_id=Issue.category_id,
        sprint_id=Issue.sprint_id,
        state_id=Issue.state_id,
        creator_id=Issue.creator_id,
        responsible_user_id=Issue.responsible_user_id,
        priority_id=Issue.priority_id,
        description=Issue.description,
        repository_link=Issue.repository_link,
        story_points=Issue.story_points,
        report_time=Issue.report_time,
        version=Issue.version,
        updater_id=Issue.updater_id,
        project_id=Issue.project_id,
        updated_at=Issue.updated_at,
        created_at=Issue.created_at,
        backlog_order_number=Issue.backlog_order_number,
        deleted_at=Issue.deleted_at,
        finisher_id=Issue.finisher_id,
        parent_issue_id=Issue.parent_issue_id,
    )

    session.add(issue_db)
    session.commit()
    session.refresh(issue_db)


def get_issues(db: Session, skip: int = 0, limit: int = 50) -> list[Issue]:

    return db.query(Issue).offset(skip).limit(limit).all()


def get_issue(session: Session, id: int) -> Issue:
    issue_db = session.query(Issue).filter(Issue.id == id).one()

    issue = Issue(
        user_id=user_db.user_id,
        username=user_db.username,
        email=user_db.email,
        created_at=user_db.created_at,
    )

    return user_response
