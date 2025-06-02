from app.db.models import Issue
from app.crud.issues import update_story_point, create_issue
from app.api.deps import SessionDep
import pytest
from sqlalchemy.exc import IntegrityError

def test_create_issue(db: SessionDep):
    """Test the creation of an issue."""
    mock_issue = Issue(
            name="Test Issue",
            category_id=1,
            sprint_id=None,
            state_id=1,
            creator_id=1,
            responsible_user_id=2,
            priority_id=3,
            description="This is a test issue.",
            repository_link="https://github.com/example/repo",
            story_points=5,
            report_time=None,
            version=1,
            updater_id=1,
            project_id=10,
            updated_at=None,
            created_at=None,
            backlog_order_number=1,
            deleted_at=None,
            finisher_id=None,
            parent_issue_id=None,
        )

    created = create_issue(db, mock_issue)

    assert created.id is not None
    assert created.name == "Test Issue"
    assert created.category_id == 1
    assert created.priority_id == 3

def test_create_issue_fails_without_name(db: SessionDep):
    issue = Issue(
        name=None,  
        project_id=1  
    )

    with pytest.raises(IntegrityError):
        created = create_issue(db, issue)

def test_update_story_point_existing(db: SessionDep):
    issue = Issue(id=1, category_id = "BUG",project_id=1, name="First Issue", story_points=3)
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
