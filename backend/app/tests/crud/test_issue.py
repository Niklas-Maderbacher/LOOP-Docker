from app.db.models import Issue
from app.crud.issue import update_story_point
from app.api.deps import SessionDep

def test_update_story_point_existing(db: SessionDep):
    issue = Issue(id=1, project_id=1, name="First Issue", story_points=3)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    updated_issue = update_story_point(db, issue_id=1, updated_story_point=13)
    
    assert updated_issue is not None
    assert updated_issue.story_points == 13
    assert updated_issue.name == "First Issue"

def test_update_story_point_nonexistent(db: SessionDep):
    updated_issue = update_story_point(db, issue_id=999, updated_story_point=7)
    
    assert updated_issue is None

def test_update_story_point_exception(db: SessionDep, monkeypatch):
    def mock_query(*args, **kwargs):
        raise ValueError("Simulated database error")
    
    monkeypatch.setattr(db, "query", mock_query)
    result = update_story_point(db, issue_id=1, updated_story_point=10)
    
    assert isinstance(result, tuple)
    error_data, status_code = result
    assert "error" in error_data
    assert "Simulated database error" in error_data["error"]
    assert status_code == 500
