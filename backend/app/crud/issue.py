from typing import Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.db.models import Issue, Attachment
from app.api.schemas.issue import IssueCreate, IssueUpdate

# Updates the story points of an issue, returns None if the issue to be changed doesn't exist in the database
def update_story_point(db: Session, issue_id:int, updated_story_point:int):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()

        issue.story_points = updated_story_point

        db.commit()
        db.refresh(issue)

        return issue

    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def create_issue(db: Session, issue_data: IssueCreate):
    issue = Issue(name=issue_data.name, project_id=issue_data.project_id)
    db.add(issue)
    db.commit()
    db.refresh(issue)

    """for link in issue_data.attachments:
        attachment = Attachment(issue_id=issue.id, link=link)
        db.add(attachment)

    db.commit()"""

    return issue

def update_issue(db: Session, issue_id: int, issue_data: IssueUpdate):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not db_issue:
        return None

    db_issue.name = issue_data.name
    
    if len(issue_data.attachments) > 0:
        for link in issue_data.attachments:
            attachment = Attachment(issue_id=db_issue.id, link=link)
            db.add(attachment)
    
    db.commit()

    return db_issue