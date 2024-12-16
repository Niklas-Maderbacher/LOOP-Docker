import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()
