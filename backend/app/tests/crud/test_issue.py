from sqlmodel import Session
from app.db.models import Issue
from app.crud.issue import update_story_point

def test_update_story_point_existing_issue(db: Session) -> None:
    existing_issue = db.query(Issue).filter(Issue.id == 1).first()

    if existing_issue is None:
        issue = Issue(id=1, project_id=1, name="Test Issue", story_points=3)
        db.add(issue)
        db.commit()
        db.refresh(issue)
    else:
        issue = existing_issue
    
    updated_issue = update_story_point(db, issue_id=1, updated_story_point=10)

    assert updated_issue is not None
    assert updated_issue.story_points == 10

def test_update_story_point_non_existing_issue(db: Session) -> None:
    result = update_story_point(db, issue_id=999, updated_story_point=5)

    assert isinstance(result, tuple)
    
    response_data, status_code = result

    assert isinstance(response_data, dict)
    assert "error" in response_data
    
    assert status_code == 500
