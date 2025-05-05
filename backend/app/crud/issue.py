from sqlmodel import Session
from app.db.models import Issue
from app.api.schemas.issue import IssueUpdate
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

# LOOP-124
def get_issues(db: Session, skip: int = 0, limit: int = 50) -> list[Issue]:
    return db.query(Issue).offset(skip).limit(limit).all()

def get_issue(session: Session, id: int) -> Issue:
    issue_db = session.query(Issue).filter(Issue.id == id).one()

    if issue_db == None:
        return None

    return issue_db
