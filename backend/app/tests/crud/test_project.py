from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Project
from app.crud.project import unarchive_project

# creates new archived project and testing to archive it 
def test_unarchive_project_success(db: Session) -> None:
    project = Project(id=999, name='Projekt1', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = unarchive_project(db, project_id=999)

    assert updated_project is not None
    assert updated_project.archived_at is None

# tests to unarchive archived project which doesn't exist 
def test_unarchive_project_not_found(db: Session) -> None:
    updated_project = unarchive_project(db, project_id=999)

    assert updated_project is None

# creates unarchived project and tests to unarchive it 
def test_unarchive_project_already_unarchived(db: Session) -> None:
    project = Project(id=99, name='Projekt2', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = unarchive_project(db, project_id=2)

    assert updated_project is None

