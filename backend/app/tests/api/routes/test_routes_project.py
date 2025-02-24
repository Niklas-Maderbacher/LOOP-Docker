import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.main import app
from app.api.routes.projects import project
from app.api.deps import SessionDep
from app.api.routes import FastApiAuthorization
from app.api.routes.FastApiAuthorization import get_current_user


# ✅ Mock User
class MockUser:
    def __init__(self, is_admin=True, email="admin@example.com", archived=False):
        self.is_admin = is_admin
        self.email = email
        self.archived = archived
        self.id = 1

# ✅ Mock Auth Dependencies
def mock_get_current_user():
    return MockUser(is_admin=True)  # Simulate Admin

def mock_get_non_admin_user():
    return MockUser(is_admin=False)  # Simulate Non-Admin

def mock_unarchive_project(session, project_id):
    return {"message": "Project successfully unarchived", "project_id": project_id}

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    return MagicMock()

# ✅ Apply Dependency Overrides for All Tests
@pytest.fixture(autouse=True)
def override_dependencies():
    # ✅ Default to an admin user
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[SessionDep] = MagicMock()  # Mock DB Session

    yield  # Run tests

    app.dependency_overrides = {}  # Cleanup after tests

def test_unarchive_project_success(mock_db_session, monkeypatch):
    project_id = 1
    monkeypatch.setattr(project, "unarchive_project", mock_unarchive_project)
    monkeypatch.setattr("app.api.deps.get_db", lambda: mock_db_session)
    
    response = client.put(f"/api/v1/projects/unarchive_project/{project_id}")
    
    assert response.status_code == 201
    assert response.json() == {
        "detail": {"message": "Project successfully unarchived", "project_id": project_id}
    }

# ✅ Test: Admin User Failure
def test_unarchive_project_failure(mock_db_session):
    mock_db_session.return_value = None
    app.dependency_overrides[project.unarchive_project] = mock_db_session

    response = client.put("/api/v1/projects/unarchive_project/2", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Could not unarchive project"}

# ✅ Test: Non-Admin User (403 Forbidden)
def test_unarchive_project_without_permission(mock_db_session, monkeypatch):
    project_id = 1

    # ✅ Override dependency to simulate a non-admin user
    app.dependency_overrides[get_current_user] = mock_get_non_admin_user

    # ✅ Mock unarchive_project behavior
    monkeypatch.setattr(project, "unarchive_project", lambda session, project_id: None)

    response = client.put(f"/api/v1/projects/unarchive_project/{project_id}", headers={"Authorization": "Bearer test_token"})

    print("Response Status Code:", response.status_code)  # Debugging
    print("Response JSON:", response.json())  # Debugging

    # ✅ Assert correct forbidden response
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}

