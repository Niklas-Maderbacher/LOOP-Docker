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
