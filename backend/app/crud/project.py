from typing import List

from sqlalchemy.orm import Session
from app.db.models import Project

def get_all_projects(db: Session, skip: int = 0, limit: int = 50) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: Project) -> Project:
  db_project = Project(**project.model_dump())
  db.add(db_project)
  db.commit()
  db.refresh(db_project)
  return db_project
