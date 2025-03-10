import pytest
from app.db.models import Project
from app.api.deps import SessionDep
from datetime import datetime

def test_unarchive_project_success(db:SessionDep, client_with_superuser):
    db_project = Project(name="Test", start_date="2025-02-02", archived_at=datetime.now())

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    print(db_project)

    response = client_with_superuser.put(f"/api/v1/projects/unarchive-project/{db_project.id}")

    assert response.status_code == 201

def test_unarchive_project_failure(db:SessionDep, client_with_superuser):
    response = client_with_superuser.put("/api/v1/projects/unarchive-project/2", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Could not unarchive project"}

def test_unarchive_project_without_permission(db:SessionDep, client):
    db_project = Project(name="Test",start_date=datetime.now())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    response = client.put(f"/api/v1/projects/unarchive-project/{db_project.id}", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}

def test_archive_project_success(db:SessionDep, client_with_superuser):
    db_project = Project(name="Test", start_date="2025-02-02")

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    print(db_project)

    response = client_with_superuser.put(f"/api/v1/projects/archive-project/{db_project.id}")

    assert response.status_code == 201

def test_archive_project_failure(db:SessionDep, client_with_superuser):
    response = client_with_superuser.put("/api/v1/projects/archive-project/2", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}

def test_archive_project_without_permission(db:SessionDep, client):
    db_project = Project(name="Test",start_date=datetime.now())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    response = client.put(f"/api/v1/projects/archive-project/{db_project.id}", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}
