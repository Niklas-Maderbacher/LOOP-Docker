from app.db.models import Issue
from app.api.deps import SessionDep

def test_update_issue_success(db: SessionDep, client_with_superuser):
    issue = Issue(id=1, project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", json={"new_story_point_value": 13}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["story_points"] == 13

def test_update_issue_negative_points(client_with_superuser, db):
    issue = Issue(id=1, project_id=1, name="First Issue", story_points=4)
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

def test_invalid_story_point_type(client_with_superuser, db):
    issue = Issue(id=1, project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(
        f"/api/v1/issues/{issue.id}", json={"new_story_point_value": "invalid"}
    )
    
    assert response.status_code == 422  # Validation error

def test_missing_required_field(client_with_superuser, db):
    issue = Issue(id=1, project_id=1, name="First Issue", story_points=4)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    response = client_with_superuser.patch(f"/api/v1/issues/{issue.id}", json={})
    
    assert response.status_code == 422


def test_create_issue_success(client, db):
    """Tests the successful creation of a issue."""
    issue = {
        "name": "First Issue",
        "category_id": 0,
        "sprint_id": 0,
        "responsible_id": 0,
        "priority_id": 0,
        "description": "NANANANA",
        "story_points": 4,
        "project_id": 0
    }
    response = client.post("/api/v1/issues/", json=issue)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "First Issue"
    assert data["description"] == "NANANANA"
    assert data["story_points"] == 4


def test_create_issue_missing_fields(client, db):
    """Tests the creation of a issue, where the required fields are empty(name, description)."""
    issue = {
        "name": "",
        "category_id": 0,
        "sprint_id": 0,
        "responsible_id": 0,
        "priority_id": 0,
        "description": "",
        "story_points": 4,
        "project_id": 0
    }

    response = client.post("/api/v1/issues/", json=issue)

    assert response.status_code == 400
    assert response.json()["detail"] == "Name and description are required fields."

def test_create_issue_invalid_story_points(client, db):
    """Tests the creation of an issue with invalid story points"""
    issue = {
        "name": "Invalid Story Points Issue",
        "category_id": 0,
        "sprint_id": 0,
        "responsible_id": 0,
        "priority_id": 0,
        "description": "Test for invalid story points",
        "story_points": -1,
        "project_id": 0
    }

    response = client.post("/api/v1/issues/", json=issue)

    assert response.status_code == 400
    assert response.json()["detail"] == "Story points need to be positive integer values."
