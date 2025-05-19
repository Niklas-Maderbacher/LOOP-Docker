import pytest
from app.db.models import User
from app.api.deps import SessionDep
from datetime import datetime

def test_get_all_users(db: SessionDep, client_with_superuser):
    db_user = User(email="user@example.com", display_name="User1", password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", is_admin=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = client_with_superuser.get(f"/api/v1/users/get_all_users")
    assert response.status_code == 200

def test_get_user_success(db: SessionDep, client_with_superuser):
    db_user = User(email="user@example.com", display_name="User1", password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", is_admin=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = client_with_superuser.get(f"/api/v1/users/get_user/{db_user.email}")
    assert response.status_code == 200

def test_get_user_failure(db: SessionDep, client_with_superuser):
    db_user = User(email="user@example.com", display_name="User1", password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", is_admin=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = client_with_superuser.get(f"/api/v1/users/get_user/admin@example.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_register_user(db: SessionDep, client_with_superuser):
    user_data = {
        "email": "test1@example.com",
        "display_name": "Test User",
        "password": "securepassword123"
    }

    response = client_with_superuser.post(f"/api/v1/users/create_user", json=user_data)

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["display_name"] == user_data["display_name"]

def test_register_user_without_permission(db: SessionDep, client):
    user_data = {
        "email": "test1@example.com",
        "display_name": "Test User",
        "password": "securepassword123"
    }

    response = client.post(f"/api/v1/users/create_user", json=user_data)

    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}
