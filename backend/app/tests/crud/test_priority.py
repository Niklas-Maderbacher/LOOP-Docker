import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Issue, User, Project
from app.crud.priority import update_priority
from app.enums.priority import Priority
from app.enums.issueType import Type


# updates the priority successfully
def test_update_priority_success(db: Session) -> None:
    # Erstelle notwendige Objekte
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    project = Project(id=1, name="Test Project", key="TEST")
    
    # Erstelle das Issue mit allen erforderlichen Feldern
    issue = Issue(
        id=1, 
        name="Test Issue", 
        category=Type.BUG,  # Verwende das Enum direkt
        project_id=1,
        priority=Priority.HIGH  # Verwende das Enum direkt
    )

    db.add_all([user, project, issue])
    db.commit()
    db.refresh(issue)

    # Führe die Funktion aus
    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="MEDIUM")

    assert updated_issue is not None
    assert updated_issue.priority == Priority.MEDIUM  # Prüfe gegen das Enum

# error: user does not exist
def test_update_priority_user_not_found(db: Session) -> None:
    updated_issue = None
    try:
        updated_issue = update_priority(db, issue_id=1, user_id=99, new_priority="HIGH")
    except ValueError as e:
        assert str(e) == "User mit ID 99 existiert nicht."

    assert updated_issue is None

# error: issue does not exist
def test_update_priority_issue_not_found(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    db.add(user)
    db.commit()
    db.refresh(user)

    updated_issue = None
    try:
        updated_issue = update_priority(db, issue_id=99, user_id=1, new_priority="HIGH")
    except ValueError as e:
        assert str(e) == "Issue mit ID 99 existiert nicht."

    assert updated_issue is None


# error: priority does not exist
def test_update_priority_invalid_priority(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    project = Project(id=1, name="Test Project", key="TEST")
    issue = Issue(
        id=1, 
        name="Test Issue", 
        category=Type.BUG,  # Füge das erforderliche Feld hinzu
        project_id=1,
        priority=Priority.HIGH
    )

    db.add_all([user, project, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = None
    try:
        updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="InvalidPriority")
    except ValueError as e:
        assert str(e) == "Priority 'InvalidPriority' existiert nicht."

    assert updated_issue is None

# error: user already has the priority
def test_update_priority_already_set(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    project = Project(id=1, name="Test Project", key="TEST")
    issue = Issue(
        id=1, 
        name="Test Issue", 
        category=Type.BUG,
        project_id=1,
        priority=Priority.HIGH
    )

    db.add_all([user, project, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="HIGH")

    assert updated_issue is not None
    assert updated_issue.priority == Priority.HIGH  # Priorität bleibt unverändert


# successfully updates the user priority
def test_update_priority_lower_priority(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    project = Project(id=1, name="Test Project", key="TEST")
    issue = Issue(
        id=1, 
        name="Test Issue", 
        category=Type.BUG,
        project_id=1,
        priority=Priority.HIGH
    )

    db.add_all([user, project, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="LOW")

    assert updated_issue is not None
    assert updated_issue.priority == Priority.LOW  # Priorität wurde erfolgreich gesenkt

# Test for updating priority with non-existing priority
def test_update_priority_priority_not_found(db: Session) -> None:
    user = User(id=1, email="testo@user.com", display_name="testo", password="Kennwort1")
    project = Project(id=1, name="Test Project", key="TEST")
    issue = Issue(
        id=1, 
        name="Test Issue", 
        category=Type.BUG,
        creator_id=1,
        project_id=1,
        priority=Priority.MEDIUM
    )
    
    db.add_all([user, project, issue])
    db.commit()
    
    with pytest.raises(ValueError, match="Priority 'Non-Existing' existiert nicht."):
        update_priority(db, issue_id=1, user_id=1, new_priority="Non-Existing")