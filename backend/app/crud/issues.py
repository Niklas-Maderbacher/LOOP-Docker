from typing import List
from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas.issue import GetIssue

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

def create_issue(session: Session, issue: Issue) -> Issue:
    issue_db = Issue(
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

    session.add(issue_db)
    session.commit()
    session.refresh(issue_db)

    return issue_db

def get_issues(db: Session) -> List[Issue]:
    return db.query(Issue).all()


def get_issue(session: Session, id: int) -> Issue:
    issue_db = session.query(Issue).filter(Issue.id == id).one()

    return issue_db
