from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Project

from app.crud.project import unarchive_project, archive_project, is_not_archived


def test_create_project(db: Session):
    """Tests the creation of a project."""
    test_Project = Project(id=1, name="LOOP", key="LOOP-001")
    db.add(test_Project)
    db.commit()
    db.refresh(test_Project)
    
    project_from_db = db.query(Project).filter(Project.id == 1).first()

    assert project_from_db.name == "LOOP"
    assert project_from_db.key == "LOOP-001"


def test_update_project(db: Session):
    """Tests updating of a project."""
    # Add Project
    test_project = Project(id=1, name="LOOP", key="LOOP-001")
    db.add(test_project)
    db.commit()
    db.refresh(test_project)
    project_from_db = db.query(Project).filter(Project.id == 1).first()
    assert project_from_db.name == "LOOP"
    assert project_from_db.key == "LOOP-001"
    
    # Update Project
    project_from_db.name = "LOOP v2"
    project_from_db.key = "LOOP-002"
    db.commit()
    db.refresh(project_from_db)

    project_from_db = db.query(Project).filter(Project.id == 1).first()
    assert project_from_db.name == "LOOP v2"
    assert project_from_db.key == "LOOP-002"


def test_remove_project(db: Session):
    """Tests the deletion of a Project"""
    # Add Project
    test_project = Project(id=1, name="LOOP", key="LOOP-001")
    db.add(test_project)
    db.commit()
    db.refresh(test_project)
    project_from_db = db.query(Project).filter(Project.id == 1).first()
    assert project_from_db.name == "LOOP"
    assert project_from_db.key == "LOOP-001"

    # Delete Project
    db.delete(test_project)
    db.commit()
    project_from_db_after_delete = db.query(Project).filter(Project.id == 1).first()
    assert project_from_db_after_delete is None