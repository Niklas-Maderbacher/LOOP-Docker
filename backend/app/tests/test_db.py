# test_config.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

# Create test database engine
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

def get_test_engine():
    """Create and return a test database engine"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        # Use PostgreSQL dialect for SQLite
        execution_options={"dialect_name": "postgresql"}
    )
    SQLModel.metadata.create_all(engine)
    return engine

def get_test_session():
    """Get a test database session"""
    engine = get_test_engine()
    with Session(engine) as session:
        yield session
