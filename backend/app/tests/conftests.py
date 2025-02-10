# /app/tests/conftest.py
 
import pytest
from sqlalchemy.orm import Session
from app.api.deps import get_db

from collections.abc import Generator
 
@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    try:
      db_session = next(get_db())  # Use your app's session
      print(f"Database session initialized: {db_session}")
      yield db_session
    except Exception as e:
        print(e)
    finally:
        db_session.close()
