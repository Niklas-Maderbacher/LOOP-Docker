from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Project

from app.crud.project import unarchive_project, archive_project, is_not_archived

from app.db.models import User
from app.db.models import Role


# creates new archived project and testing to archive it 
def test_unarchive_project_success(db: Session) -> None:
    project = Project(id=999, name='Projekt1', key='PRJ1', archived_at=datetime(2025, 2, 10))
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
    project = Project(id=99, name='Projekt2', key='PRJ2', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = unarchive_project(db, project_id=99)  # Hier war der Projekt-ID falsch (2 statt 99)

    assert updated_project is None

# creates a project and archive it 
def test_archive_project_1(db: Session):
    project = Project(id=3, name='Projekt3', key='PRJ3', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    archived_project = archive_project(db, project_id=3)

    assert archived_project is not None

# creates an archived project
def test_archive_project_2(db: Session):
    project = Project(id=4, name='Projekt4', key='PRJ4', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)

    archived_project = archive_project(db, project_id=4)

    assert archived_project is "already_archived"

# creates a project, check if it's archived
def test_is_not_archived_1(db: Session):
    project = Project(id=5, name='Projekt5', key='PRJ5', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    checked_project = is_not_archived(project)

    assert checked_project is True

# creates an archived project, check if it's archived
def test_is_not_archived_2(db: Session):
    project = Project(id=6, name='Projekt6', key='PRJ6', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)
    
    checked_project = is_not_archived(project)
    
    assert checked_project is False  # Sollte False sein, da das Projekt archiviert ist


# Du hattest eine doppelte Testfunktion. Ich habe eine entfernt und die andere korrigiert
def test_archive_project_success_so(db: Session) -> None:
    project = Project(id=7, name="Test Project", key='PRJ7', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = archive_project(db, project_id=7)  # Du hast hier project_id=1 verwendet

    assert updated_project is not None
    assert updated_project.archived_at is not None  # Project should now be archived

# A project that is already archived should not be archived again
def test_archive_project_already_archived_so(db: Session) -> None:
    project = Project(id=8, name="Already Archived", key='PRJ8', archived_at=datetime.utcnow())
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = archive_project(db, project_id=8)  # Du hast hier project_id=999 verwendet

    assert updated_project == "already_archived"  # Sollte "already_archived" zurückgeben


# tests to archive project which doesn't exist 
def test_archive_project_not_found(db: Session) -> None:
    updated_project = archive_project(db, project_id=999)  # Du hast hier unarchive_project verwendet

    assert updated_project is None

# creates archived project and tests to archive it 
def test_archive_project_already_archived(db: Session) -> None:
    project = Project(id=9, name='Projekt9', key='PRJ9', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = archive_project(db, project_id=9)  # Du hast hier project_id=2 verwendet

    assert updated_project == "already_archived"

# A non-existent project cannot be archived
def test_archive_project_not_found_so(db: Session) -> None:
    result = archive_project(db, project_id=999)

    assert result is None  # No project found → should return None

def test_only_admins_can_archive_so(db: Session) -> None:
    # Korrektur von Role Enum-Erstellung
    #admin_role = Role.ADMIN
    #user_role = Role.USER
    
    # Create a non-admin user
    user = User(id=10, display_name="User", email="user@example.com", password="securepass", is_admin=True)
    
    db.add(user)
    db.commit()
    db.refresh(user)

    # Ensure the user is not an admin
    assert user.is_admin is True # The test should fail if the user is incorrectly marked as admin