import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.main import app
from app.api.routes.issues import router
from app.api.deps import SessionDep
from app.db.models import Issue

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture(autouse=True)
def override_dependencies():
    # Mock the database session
    app.dependency_overrides[SessionDep] = MagicMock()

    yield  # Run tests

    app.dependency_overrides = {}  # Cleanup after tests

def mock_update_story_points(session, issue_id, new_story_point_value):
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if new_story_point_value < 0:
        raise HTTPException(status_code=400, detail="Story points must be a positive integer")
    issue.story_points = new_story_point_value
    session.commit()
    session.refresh(issue)
    return issue

def test_update_story_points_success(mock_db_session, monkeypatch):
    # Mock the update_story_points function
    monkeypatch.setattr(router, "update_story_points", mock_update_story_points)
    monkeypatch.setattr("app.api.deps.get_db", lambda: mock_db_session)

    # Mock the database query to return a test issue
    test_issue = Issue(id=1, project_id=1, name="Test Issue", story_points=3)
    mock_db_session.query.return_value.filter.return_value.first.return_value = test_issue

    # Make the PATCH request
    response = client.patch(
        "/api/v1/issues/1",
        json={"new_story_point_value": 5}
    )

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "project_id": 1,
        "name": "Test Issue",
        "story_points": 5
    }

def test_update_non_existing_issue(mock_db_session, monkeypatch):
    # Mock the update_story_points function
    monkeypatch.setattr(router, "update_story_points", mock_update_story_points)
    monkeypatch.setattr("app.api.deps.get_db", lambda: mock_db_session)

    # Mock the database query to return None (issue not found)
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Make the PATCH request
    response = client.patch(
        "/api/v1/issues/999",
        json={"new_story_point_value": 5}
    )

    # Assert the response
    assert response.status_code == 404
    assert response.json() == {"detail": "Issue not found"}

def test_negative_story_points(mock_db_session, monkeypatch):
    # Mock the update_story_points function
    monkeypatch.setattr(router, "update_story_points", mock_update_story_points)
    monkeypatch.setattr("app.api.deps.get_db", lambda: mock_db_session)

    # Mock the database query to return a test issue
    test_issue = Issue(id=1, project_id=1, name="Test Issue", story_points=3)
    mock_db_session.query.return_value.filter.return_value.first.return_value = test_issue

    # Make the PATCH request with negative story points
    response = client.patch(
        "/api/v1/issues/1",
        json={"new_story_point_value": -5}
    )

    # Assert the response
    assert response.status_code == 400
    assert response.json() == {"detail": "Story points must be a positive integer"}