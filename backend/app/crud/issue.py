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
