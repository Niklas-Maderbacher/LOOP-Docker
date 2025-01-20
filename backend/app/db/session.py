import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import settings


DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()
