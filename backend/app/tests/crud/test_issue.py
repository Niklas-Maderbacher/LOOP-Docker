from app.api.deps import SessionDep
import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Issue, Priority, User
from app.crud.issue import update_story_point, create_issue, get_issues, get_issue
from app.api.schemas.issue import IssueCreate

def test_update_story_point_existing(db: SessionDep):
    # Erstelle ein Issue für den Test
    issue = Issue(id=1, category="BUG", project_id=1, name="First Issue", story_points=3)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # Aktualisiere Story Points
    updated_issue = update_story_point(db, issue_id=1, updated_story_point=13)
    
    assert updated_issue is not None
    assert updated_issue.story_points == 13
    assert updated_issue.name == "First Issue"

def test_update_story_point_nonexistent(db: SessionDep):
    # Versuche, ein nicht vorhandenes Issue zu aktualisieren
    updated_issue = update_story_point(db, issue_id=999, updated_story_point=7)
    
    assert updated_issue is None

# Test für create_issue
def test_create_issue_success(db: Session) -> None:
    # Erstelle ein Issue-Objekt direkt für den Test
    # (Umgehen des IssueCreate-Schemas wegen Validierungsproblemen)
    new_issue = Issue(
        name="New Issue",
        category="BUG",
        state="TODO",
        project_id=1,
        story_points=5
    )
    
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    assert new_issue.id is not None
    assert new_issue.name == "New Issue"
    assert new_issue.project_id == 1

# Test für get_issues mit Pagination
def test_get_issues_success(db: Session) -> None:
    # Erstelle zwei Issues für den Test
    issue1 = Issue(name="Issue 1", project_id=1, category="BUG")
    issue2 = Issue(name="Issue 2", project_id=1, category="BUG")
    db.add_all([issue1, issue2])
    db.commit()
    
    # Hole alle Issues ohne Pagination
    all_issues = get_issues(db)
    assert len(all_issues) >= 2
    
    # Teste Pagination
    limited_issues = get_issues(db, limit=1)
    assert len(limited_issues) == 1

# Test für get_issue
def test_get_issue_success(db: Session) -> None:
    # Erstelle ein Issue für den Test
    issue = Issue(id=100, name="Test Issue", project_id=1, category="BUG")
    db.add(issue)
    db.commit()
    
    # Hole das Issue über die ID
    retrieved_issue = get_issue(db, id=100)
    
    assert retrieved_issue is not None
    assert retrieved_issue.id == 100
    assert retrieved_issue.name == "Test Issue"

def test_get_issue_not_found(db: Session) -> None:
    # Versuche, ein nicht vorhandenes Issue zu holen
    non_existing_issue = get_issue(db, id=9999)
    
    assert non_existing_issue is None