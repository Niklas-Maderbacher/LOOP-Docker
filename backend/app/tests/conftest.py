# /app/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from app.api.deps import get_db
from app.api.routes.FastApiAuthorization import get_current_user
from app.db.models import User
from app.main import app
from datetime import datetime

# ✅ Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"  # ✅ Use a file-based DB (more stable)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def db():
    """Creates a new database session and ensures tables exist."""
    SQLModel.metadata.create_all(engine)  
    session = TestingSessionLocal()
    try:
        yield session  
    finally:
        session.rollback()
        session.close()
        SQLModel.metadata.drop_all(bind=engine)  

@pytest.fixture(scope="function")
def client(db):
    """Provides a FastAPI test client using the same session as the test."""
    
    def override_get_db():
        SQLModel.metadata.create_all(engine)
        yield db  # ✅ Use the same session from the test fixture

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_superuser(db):
    """Creates a superuser in the test database."""
    user = User(id=1, username="superuser", email="superuser@example.com", display_name="Super User", password="dSDDSADSA", created_at=datetime.now(), is_admin=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def client_with_superuser(client, test_superuser, db):
    """Override `get_current_active_superuser` to return an admin user."""
    
    def override_get_current_user():
        return db.merge(test_superuser)
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client