# /app/tests/conftest.py

import pytest
from sqlalchemy.orm import Session
from app.api.deps import get_db

@pytest.fixture(scope="function")
def db() -> Session:
    db_session = next(get_db())  # Use your app's session
    try:
        yield db_session
    finally:
        db_session.close()
