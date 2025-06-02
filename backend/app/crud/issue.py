from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas.issue import IssueCreate

def update_story_point(db: Session, issue_id: int, updated_story_point: int):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:  
            return None  
        issue.story_points = updated_story_point
        db.commit()
        db.refresh(issue)
        
        return issue
    except Exception as e:
        db.rollback()
        print(f"Error updating story point: {str(e)}")
        return None




def create_issue(session: Session, issue_data: IssueCreate) -> Issue:
    """
    Erstellt ein neues Issue in der Datenbank.
    
    Args:
        session: Datenbanksitzung
        issue_data: Issue-Daten vom IssueCreate Schema
        
    Returns:
        Das erstellte Issue
    """
    issue_db = Issue(
        name=issue_data.name,
        category=issue_data.category,
        state=issue_data.state,
        sprint_id=issue_data.sprint_id,
        responsible_user_id=issue_data.responsible_user_id,
        priority=issue_data.priority,
        description=issue_data.description,
        story_points=issue_data.story_points,
        project_id=issue_data.project_id
    )
    
    session.add(issue_db)
    session.commit()
    session.refresh(issue_db)
    
    return issue_db



def get_issues(db: Session, skip: int = 0, limit: int = 50) -> list[Issue]:
    return db.query(Issue).offset(skip).limit(limit).all()

def get_issue(session: Session, id: int) -> Issue:
    return session.query(Issue).filter(Issue.id == id).first()

