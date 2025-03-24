from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Project

from app.crud.priority import update_priority

from app.db.models import User
from app.db.models import Priority
from app.db.models import Issue

from sqlalchemy.orm import Session
from app.db.models import Priority, Issue, User

# updates the priority successfully
def test_update_priority_success(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    priority = Priority(id=1, name="High")
    issue = Issue(id=1, name="Test Issue", priority_id=1, project_id=1)

    db.add_all([user, priority, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="High")

    assert updated_issue is not None
    assert updated_issue.priority_id == priority.id

# error: user does not exist
def test_update_priority_user_not_found(db: Session) -> None:
    updated_issue = None
    try:
        updated_issue = update_priority(db, issue_id=1, user_id=99, new_priority="High")
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
        updated_issue = update_priority(db, issue_id=99, user_id=1, new_priority="High")
    except ValueError as e:
        assert str(e) == "Issue mit ID 99 existiert nicht."

    assert updated_issue is None

# error: priority does not exist
def test_update_priority_invalid_priority(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    issue = Issue(id=1, name="Test Issue", priority_id=1, project_id=1)

    db.add_all([user, issue])
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
    priority = Priority(id=1, name="High")
    issue = Issue(id=1, name="Test Issue", priority_id=1, project_id=1)

    db.add_all([user, priority, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="High")

    assert updated_issue is not None
    assert updated_issue.priority_id == priority.id  # Priorität bleibt unverändert


# successfully updates the user priority
def test_update_priority_lower_priority(db: Session) -> None:
    user = User(id=1, email="test@example.com", display_name="Test User", password="securepass")
    priority_high = Priority(id=1, name="High")
    priority_low = Priority(id=2, name="Low")
    issue = Issue(id=1, name="Test Issue", priority_id=1, project_id=1)

    db.add_all([user, priority_high, priority_low, issue])
    db.commit()
    db.refresh(issue)

    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority="Low")

    assert updated_issue is not None
    assert updated_issue.priority_id == priority_low.id  # Priorität wurde erfolgreich gesenkt
