from sqlmodel import Session, create_engine, select

from app.config.config import settings


DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

# SQLAlchemy
engine = create_engine(DATABASE_URL)

# creating tables using SQLModel

from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
