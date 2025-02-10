from sqlmodel import Session
from app.db.models import Issue
from app.crud.issue import update_story_point

def test_update_story_point_existing_issue(db: Session) -> None:
    issue = Issue(id=1, title="Test Issue", story_points=3)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    updated_issue = update_story_point(db, issue_id=1, updated_story_point=5)
    
    assert updated_issue is not None
    assert updated_issue.story_points == 5

def test_update_story_point_non_existing_issue(db: Session) -> None:
    result = update_story_point(db, issue_id=999, updated_story_point=5)
    
    assert isinstance(result, dict)
    assert "error" in result
