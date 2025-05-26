# tests/api/routes/test_issues.py

from app.api.schemas.issue import StoryPointUpdate
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import SessionDep
from app.db.models import Issue

client = TestClient(app)

def test_update_issue_story_points_success(db: SessionDep, client_with_superuser):
    """
    Test für das erfolgreiche Aktualisieren von Story Points eines Issues.
    """
    # Erstelle einen Test-Issue in der Datenbank
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # Sende die Update-Anfrage
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", 
        json={"new_story_point_value": 5}
    )
    
    # Überprüfe die Antwort
    assert response.status_code == 200
    updated_issue = response.json()
    assert updated_issue["story_points"] == 5

def test_update_issue_story_points_failure_negative_value(db: SessionDep, client_with_superuser):
    """
    Test für das Fehlschlagen des Aktualisierens von Story Points mit einem negativen Wert.
    """
    # Erstelle einen Test-Issue in der Datenbank
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # Sende die Update-Anfrage mit einem negativen Wert
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", 
        json={"new_story_point_value": -1}
    )
    
    # Überprüfe die Antwort
    assert response.status_code == 400
    assert "Story points need to be positive integer" in response.json()["detail"]

def test_update_issue_story_points_no_update(db: SessionDep, client_with_superuser):
    """
    Test für keine Aktualisierung der Story Points, wenn der neue Wert gleich dem aktuellen ist.
    """
    # Erstelle einen Test-Issue in der Datenbank
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=0)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # Sende die Update-Anfrage mit dem gleichen Wert
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", 
        json={"new_story_point_value": 0}
    )
    
    # Überprüfe die Antwort
    assert response.status_code == 200
    updated_issue = response.json()
    assert updated_issue["story_points"] == 0

def test_update_issue_success(db: SessionDep, client_with_superuser):
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", json={"new_story_point_value": 13}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["story_points"] == 13


def test_update_issue_negative_points(db: SessionDep, client_with_superuser):
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(
       f"/api/v1/issues/{issue.id}", json={"new_story_point_value": -3}
    )
    
    assert response.status_code == 400
    assert "Story points need to be positive integer" in response.json()["detail"]

def test_update_nonexistent_issue(client_with_superuser):
    response = client_with_superuser.patch(
        "/api/v1/issues/999", json={"new_story_point_value": 5}
    )
    
    assert response.status_code == 204
    assert response.content == b''


def test_invalid_story_point_type(db: SessionDep, client_with_superuser):
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", json={"new_story_point_value": "invalid"}
    )
    
    assert response.status_code == 422  # Validierungsfehler

def test_missing_required_field(db: SessionDep, client_with_superuser):
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(f"/api/v1/issues/{issue.id}", json={})
    
    assert response.status_code == 422


def test_create_issue_success(client):
    """Tests die erfolgreiche Erstellung eines Issues."""

    issue = {
        "name": "First Issue",
        "category": "Bug",  
        "state": "Blocked",  
        "sprint_id": 0,
        "responsible_user_id": 0,
        "priority": "High", 
        "description": "NANANANA",
        "story_points": 4,
        "project_id": 0
    }
    response = client.post("/api/v1/issues/create", json=issue)
    
    print("Response:", response.status_code)
    print("Response content:", response.json())
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "First Issue"
    assert data["description"] == "NANANANA"
    assert data["story_points"] == 4

def test_create_issue_missing_fields(client):
    """Tests die Erstellung eines Issues, bei dem die erforderlichen Felder leer sind (Name, Beschreibung)."""
    issue = {
        "name": "",
        "category": "User Story",
        "state": "To Do",
        "sprint_id": 0,
        "responsible_user_id": 0,
        "priority": "High",
        "description": "",
        "story_points": 4,
        "project_id": 0
    }

    response = client.post("/api/v1/issues/create", json=issue)

    assert response.status_code == 400
    assert response.json()["detail"] == "Name and description are required fields."

def test_create_issue_invalid_story_points(client):
    """Tests die Erstellung eines Issues mit ungültigen Story Points"""
    issue = {
        "name": "Invalid Story Points Issue",
        "category": "User Story",
        "state": "To Do",
        "sprint_id": 0,
        "responsible_user_id": 0,
        "priority": "High",
        "description": "Test for invalid story points",
        "story_points": -1,
        "project_id": 0
    }

    response = client.post("/api/v1/issues/create", json=issue)

    assert response.status_code == 400
    assert response.json()["detail"] == "Story points need to be positive integer values."