import pytest
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

# API Tests
class TestIssueApi:
    def test_update_issue_success(self, client, session):
        # Test successful update via API
        response = client.patch(
            "/issues/2",
            json={"new_story_point_value": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["story_points"] == 10
        
        # Verify database was updated
        updated_issue = session.query(Issue).filter(Issue.id == 2).first()
        assert updated_issue.story_points == 10
    
    def test_update_issue_negative_points(self, client):
        response = client.patch(
            "/issues/1",
            json={"new_story_point_value": -3}
        )
        
        assert response.status_code == 400
        assert "Story points need to be positive integer" in response.json()["detail"]
    
    def test_update_nonexistent_issue(self, client):
        response = client.patch(
            "/issues/999",
            json={"new_story_point_value": 5}
        )
        
        assert response.status_code == 204
        assert response.content == b''  # Empty response for 204
    
    def test_invalid_story_point_type(self, client):
        # Test with non-integer story point
        response = client.patch(
            "/issues/1",
            json={"new_story_point_value": "invalid"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_missing_required_field(self, client):
        # Test with missing required field
        response = client.patch("/issues/1", json={})
        
        assert response.status_code == 422
