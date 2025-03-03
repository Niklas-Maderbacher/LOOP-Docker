# /app/tests/conftest.py

import pytest
from sqlalchemy.orm import Session
from app.api.deps import get_db
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from app.main import app
from app.api.deps import SessionDep
from test_db import get_test_engine, get_test_session

@pytest.fixture(scope="function")
def db() -> Session:
    db_session = next(get_db())  # Use your app's session
    try:
        yield db_session
    finally:
        db_session.close()

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
def client_fixture(session, db):
    def get_session_override():
        yield db

    app.dependency_overrides = {
        SessionDep: get_test_session,
    }
    
    return TestClient(app)
    
    app.dependency_overrides = {}
