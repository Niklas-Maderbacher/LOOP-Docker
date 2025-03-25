from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas.issue import IssueCreate

def update_story_point(db: Session, issue_id: int, updated_story_point: int):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()

        if not issue:  # Issue does not exist
            return None  

        issue.story_points = updated_story_point
        db.commit()
        print(f"Updated issue {issue_id}: {issue.story_points}")
        db.refresh(issue)
        
        return issue

    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def create_issue(db: Session, issue: IssueCreate) -> Issue:
    """Creates a new issue in the database.

    Args:
        db (Session): Database session
        issue (IssueCreate): Issue details

    Returns:
        Issue: The created issue instance
    """
    db_issue = Issue(
        name=issue.name,
        category_id=issue.category_id,
        sprint_id=issue.sprint_id,
        responsible_user_id=issue.responsible_id,
        priority_id=issue.priority_id,
        description=issue.description,
        story_points=issue.story_points,
        project_id=issue.project_id
    )

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

def get_issues(db: Session, skip: int = 0, limit: int = 50) -> list[Issue]:

    return db.query(Issue).offset(skip).limit(limit).all()


def get_issue(session: Session, id: int) -> Issue:
    issue_db = session.query(Issue).filter(Issue.id == id).one()

    issue_db = Issue(
        id=issue_db.id,
        name=issue_db.name,
        category_id=issue_db.category_id,
        sprint_id=issue_db.sprint_id,
        state_id=issue_db.state_id,
        creator_id=issue_db.creator_id,
        responsible_user_id=issue_db.responsible_user_id,
        priority_id=issue_db.priority_id,
        description=issue_db.description,
        repository_link=issue_db.repository_link,
        story_points=issue_db.story_points,
        report_time=issue_db.report_time,
        version=issue_db.version,
        updater_id=issue_db.updater_id,
        project_id=issue_db.project_id,
        updated_at=issue_db.updated_at,
        created_at=issue_db.created_at,
        backlog_order_number=issue_db.backlog_order_number,
        deleted_at=issue_db.deleted_at,
        finisher_id=issue_db.finisher_id,
        parent_issue_id=issue_db.parent_issue_id,
    )

    return issue_db

