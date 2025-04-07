from app.api.deps import SessionDep
import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Issue, Priority, User
from app.crud.issue import update_story_point, create_issue, get_issues, get_issue



def test_update_story_point_existing(db: SessionDep):
    issue = Issue(id=1, project_id = 1, name="First Issue", story_points=3)
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
    
# Test for updating story points
def test_update_story_point_success(db: Session) -> None:
    issue = Issue(id=1, name="Test Issue", story_points=5, project_id=1)
    db.add(issue)
    db.commit()
    
    updated_issue = update_story_point(db, issue_id=1, updated_story_point=8)
    
    assert updated_issue.story_points == 8

# Test for updating story points with non-existing issue
def test_update_story_point_not_found(db: Session) -> None:
    updated_issue = update_story_point(db, issue_id=999, updated_story_point=8)
    
    assert updated_issue is None

# Test for retrieving issues
def test_get_issues_success(db: Session) -> None:
    issue1 = Issue(name="Issue 1", project_id=1)
    issue2 = Issue(name="Issue 2", project_id=1)
    db.add_all([issue1, issue2])
    db.commit()
    
    issues = get_issues(db)
    
    assert len(issues) == 2

test_user = User(
        email="testuser@example.com",
        display_name="Test User",
        password="testpassword123",  # Normalerweise würdest du das Passwort hashen
        microsoft_account=False,
        is_email_verified=True,
        is_admin=False)

# Test for creating an issue
def test_create_issue_success(db: Session) -> None:
    issue3 = Issue(name= "New Issue", creator_id=1, priority_id=1,  project_id=1)
    created_issue = create_issue(db, issue3)
    
    assert created_issue.id is not None


# Test for retrieving a single issue
def test_get_issue_success(db: Session) -> None:
    issue = Issue(id=1, name="Test Issue", project_id=1)
    db.add(issue)
    db.commit()
    
    retrieved_issue = get_issue(db, id=1)
    
    assert retrieved_issue.id == 1
    assert retrieved_issue.name == "Test Issue"