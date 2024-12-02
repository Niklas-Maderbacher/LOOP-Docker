"""Database Classes named tableDB"""

from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from db.session import engine

Base = declarative_base()


class IssueDB(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    issue_type = Column(String(50), nullable=False)
    title = Column(String(50), nullable=False)
    report_time = Column(String(50))
    task_point = Column(Integer, nullable=True)


Base.metadata.create_all(engine)
