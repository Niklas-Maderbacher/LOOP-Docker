import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Issue, Priority, User
from app.crud.priority import update_priority

# Test for updating priority
def test_update_priority_success(db: Session) -> None:
    user = User(id=1, email = "testo@user.com", display_name = "testo", password = "Kennwort1")
    priority = Priority(id=1, name="High")
    issue = Issue(id=1, name="Test Issue", priority_id=1, creator_id=1, version=1, project_id=1)
    
    db.add_all([user, priority, issue])
    db.commit()
    
    db.refresh(user)
    db.refresh(priority)
    db.refresh(issue)
    
    
    updated_issue = update_priority(db, issue_id=1, user_id=1, new_priority_name="High")
    
    assert updated_issue.priority_id == priority.id
    assert updated_issue.version == issue.version + 1

# Test for updating priority with non-existing user
def test_update_priority_user_not_found(db: Session) -> None:
    with pytest.raises(ValueError, match="User mit ID 999 existiert nicht."):
        update_priority(db, issue_id=1, user_id=999, new_priority_name="High")

# Test for updating priority with non-existing issue
def test_update_priority_issue_not_found(db: Session) -> None:
    user = User(id=1, email = "testo@user.com", display_name = "testo", password = "Kennwort1")
    db.add(user)
    db.commit()
    
    with pytest.raises(ValueError, match="Issue mit ID 999 existiert nicht."):
        update_priority(db, issue_id=999, user_id=1, new_priority_name="High")

# Test for updating priority with non-existing priority
def test_update_priority_priority_not_found(db: Session) -> None:
    user = User(id=1, email = "testo@user.com", display_name = "testo", password = "Kennwort1")
    issue = Issue(id=1, name="Test Issue", priority_id=2, creator_id=1, project_id = 1)
    db.add_all([user, issue])
    db.commit()
    
    with pytest.raises(ValueError, match="Priority 'Non-Existing' existiert nicht."):
        update_priority(db, issue_id=1, user_id=1, new_priority_name="Non-Existing")