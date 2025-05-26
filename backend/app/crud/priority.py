from sqlmodel import Session
from app.db.models import Issue, User
from app.enums.priority import Priority
from datetime import datetime

def update_priority(db: Session, issue_id: int, user_id: int, new_priority: str):
    """
    Aktualisiert die Priorität eines Issues.
    
    Args:
        db (Session): Datenbank-Session
        issue_id (int): ID des zu aktualisierenden Issues
        user_id (int): ID des Benutzers, der die Aktualisierung durchführt
        new_priority (str): Name der neuen Priorität
        
    Returns:
        Issue: Aktualisiertes Issue-Objekt oder None, wenn ein Fehler auftritt
        
    Raises:
        ValueError: Wenn Benutzer, Issue oder Priorität nicht existieren
    """
    # Überprüfen, ob der User existiert
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User mit ID {user_id} existiert nicht.")

    # Überprüfen, ob das Issue existiert
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise ValueError(f"Issue mit ID {issue_id} existiert nicht.")

    # Versuche, die Priority aus dem Enum zu erhalten
    try:
        # Konvertiere zu Großbuchstaben für Konsistenz mit Enum-Namen
        priority_enum = Priority[new_priority.upper()]
    except (KeyError, AttributeError):
        raise ValueError(f"Priority '{new_priority}' existiert nicht.")

    # Wenn die Priorität bereits gesetzt ist, nichts ändern
    if issue.priority == priority_enum:
        return issue

    # Priorität aktualisieren
    issue.priority = priority_enum
    issue.updater_id = user_id
    issue.updated_at = datetime.utcnow().isoformat()
    
    # Version erhöhen, falls vorhanden
    if hasattr(issue, 'version') and issue.version is not None:
        issue.version += 1
    elif hasattr(issue, 'version'):
        issue.version = 1

    db.commit()
    db.refresh(issue)

    return issue