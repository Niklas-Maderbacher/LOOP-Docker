import pytest
from sqlmodel import Session
from app.db.models import Issue
from app.crud.issue import update_story_point
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.main import app
from app.api.deps import SessionDep
from app.db.models import Issue

# Import the test configuration
from test_db import get_test_engine, get_test_session

# Create test engine and setup/teardown
@pytest.fixture(name="engine")
def engine_fixture():
    engine = get_test_engine()
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides = {
        SessionDep: get_test_session,
    }
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides = {}

# Test data fixtures
@pytest.fixture(name="test_issues")
def test_issues_fixture(session):
    # Create multiple test issues
    issues = [
        Issue(id=1, project_id=1, name="First Issue", story_points=3),
        Issue(id=2, project_id=1, name="Second Issue", story_points=5),
        Issue(id=3, project_id=2, name="Third Issue", story_points=8),
    ]
    
    for issue in issues:
        session.add(issue)
    
    session.commit()
    
    for issue in issues:
        session.refresh(issue)
    
    return issues

# CRUD Tests
class TestIssueCrud:
    def test_update_story_point_existing(self, session):
        # Test updating an existing issue
        updated = update_story_point(session, issue_id=1, updated_story_point=13)
        assert updated is not None
        assert updated.story_points == 13
        assert updated.name == "First Issue"
    
    def test_update_story_point_nonexistent(self, session):
        # Test updating a non-existent issue
        result = update_story_point(session, issue_id=999, updated_story_point=7)
        assert result is None
    
    def test_update_story_point_exception(self, session, monkeypatch):
        # Test exception handling by forcing an error
        def mock_query(*args, **kwargs):
            raise ValueError("Simulated database error")
        
        monkeypatch.setattr(session, "query", mock_query)
        result = update_story_point(session, issue_id=1, updated_story_point=10)
        
        assert isinstance(result, tuple)
        error_data, status_code = result
        assert "error" in error_data
        assert "Simulated database error" in error_data["error"]
        assert status_code == 500
