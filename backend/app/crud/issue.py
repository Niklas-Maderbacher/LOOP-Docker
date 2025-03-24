from typing import List
from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas import IssueGet

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

    return issue_db

def get_issues(db: Session) -> List[IssueGet]:
    issues = db.query(Issue).all()
    
    return [
        IssueGet(
            name=issue.title, 
            priority_id=issue.priority, 
            story_points=issue.story_points, 
            responsible_user_id=issue.assignee
        )
        for issue in issues
    ]


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
