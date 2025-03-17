from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Project

from app.crud.project import unarchive_project, archive_project, is_not_archived

from app.db.models import User
from app.db.models import Role

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

# creates a project and archive it 
def test_archive_project_1(db: Session):
    project = Project(id=3, name='Projekt3', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    archived_project = archive_project(db, project_id=3)

    assert archived_project is not None

# creates an archived project
def test_archive_project_2(db: Session):
    project = Project(id=4, name='Projekt4', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)

    archived_project = archive_project(db, project_id=4)

    assert archived_project is "already_archived"

# creates a project, check if it's archived
def test_is_not_archived_1(db: Session):
    project = Project(id=5, name='Projekt5', archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    checked_project = is_not_archived(project)

    assert checked_project is True

# creates an archived project, check if it's archived
def test_is_not_archived_2(db: Session):
    project = Project(id=6, name='Projekt6', archived_at=datetime(2025, 2, 10))



# Successfully archive an active project as an admin
def test_archive_project_success_so(db: Session) -> None:
    project = Project(id=1, name="Test Project", archived_at=None)
    db.add(project)
    db.commit()
    db.refresh(project)

    checked_project = is_not_archived(project)

    assert checked_project is False

# creates new project and testing to archive it 
def test_archive_project_success_so(db: Session) -> None:
    project = Project(id=999, name='Projekt1')
    updated_project = archive_project(db, project_id=1)

    assert updated_project is not None
    assert updated_project.archived_at is not None  # Project should now be archived

# A project that is already archived should not be archived again
def test_archive_project_already_archived_so(db: Session) -> None:
    project = Project(id=2, name="Already Archived", archived_at=datetime.utcnow())
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = archive_project(db, project_id=999)

    assert updated_project is not None
    assert updated_project.archived_at is not None


# tests to archive project which doesn't exist 
def test_archive_project_not_found(db: Session) -> None:
    updated_project = unarchive_project(db, project_id=999)

    assert updated_project is None

# creates archived project and tests to archive it 
def test_archive_project_already_archived(db: Session) -> None:
    project = Project(id=99, name='Projekt2', archived_at=datetime(2025, 2, 10))
    db.add(project)
    db.commit()
    db.refresh(project)

    updated_project = archive_project(db, project_id=2)

    assert updated_project is None

    result = archive_project(db, project_id=2)

    assert result == "already_archived"

# A non-existent project cannot be archived
def test_archive_project_not_found_so(db: Session) -> None:
    result = archive_project(db, project_id=999)

    assert result is None  # No project found → should return None

def test_only_admins_can_archive_so(db: Session) -> None:
    # Create role entries in the database if they don't exist
    admin_role = Role(id=1, name="admin")
    user_role = Role(id=2, name="user")
    
    db.add_all([admin_role, user_role])
    db.commit()

    # Create a non-admin user
    user = User(id=10, display_name="Regular User", email="user@example.com", password="securepass", is_admin=False)
    
    db.add(user)
    db.commit()
    db.refresh(user)

    # Ensure the user is not an admin
    assert not user.is_admin  # The test should fail if the user is incorrectly marked as admin
