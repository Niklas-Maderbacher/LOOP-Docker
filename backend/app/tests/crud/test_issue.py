from app.crud.issue import update_story_point
from app.api.deps import SessionDep
import pytest
from sqlmodel import Session
from app.db.models import Issue, Priority, User
from app.crud.issue import create_issue, get_issues, get_issue
from app.crud.priority import update_priority
from datetime import datetime

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



def test_create_issue(db: Session):
    issue_data = Issue(
        name="Test Issue",
        category_id=1,
        sprint_id=1,
        state_id=1,
        creator_id=1,
        responsible_user_id=2,
        priority_id=1,
        description="Test description",
        repository_link="http://github.com/test",
        story_points=5,
        report_time=datetime.utcnow(),
        version=1,
        updater_id=1,
        project_id=1,
        updated_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        backlog_order_number=1,
        deleted_at=None,
        finisher_id=None,
        parent_issue_id=None,
    )
    
    created_issue = create_issue(db, issue_data)
    assert created_issue is not None
    assert created_issue.name == "Test Issue"

def test_get_issues(db: Session):
    issues = get_issues(db)
    assert isinstance(issues, list)

def test_get_issue(db: Session):
    issue = Issue(id=1, name="Existing Issue", category_id=1, project_id=1)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    fetched_issue = get_issue(db, id=1)
    assert fetched_issue is not None
    assert fetched_issue.name == "Existing Issue"

def test_update_priority(db: Session):
    user = User(id=1, name="Test User")
    priority = Priority(id=1, name="High")
    issue = Issue(id=1, name="Issue to Update", category_id=1, priority_id=2, creator_id=1, project_id=1)
    
    db.add(user)
    db.add(priority)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    updated_issue = update_priority(issue_id=1, user_id=1, new_priority_name="High")
    assert updated_issue is not None
    assert updated_issue.priority_id == 1
