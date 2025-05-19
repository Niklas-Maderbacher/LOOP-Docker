from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas.issue import IssueUpdate, IssueCreate
from datetime import datetime

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


# LOOP-124
def update_issue(db: Session, issue_id: int, update_data: IssueUpdate):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not db_issue:
        raise None

    update_dict = update_data.dict(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_issue, key, value) 
    
    db_issue.updated_at = datetime.now() 
    db_issue.version = db_issue.version + 1 

    db.commit()
    db.refresh(db_issue)
    return db_issue


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
        category=issue.category,
        sprint_id=issue.sprint_id,
        responsible_user_id=issue.responsible_id,
        priority_id=issue.priority_id,
        description=issue.description,
        story_points=issue.story_points,
        project_id=issue.project_id,
        created_at= datetime.now
    )

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

# LOOP-124
def get_issues(db: Session, skip: int = 0, limit: int = 50) -> list[Issue]:
    return db.query(Issue).offset(skip).limit(limit).all()

def get_issue(session: Session, id: int) -> Issue:
    issue_db = session.query(Issue).filter(Issue.id == id).one()

    if issue_db == None:
        return None

    return issue_db

