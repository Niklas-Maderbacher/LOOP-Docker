from fastapi import APIRouter, HTTPException, Depends
from app.api.routes import FastApiAuthorization
from app.crud.priority import update_priority  



router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/update-priority")
def update_issue_priority(issue_id: int, user_id: int, priority_name: str):
    """
    Ruft die CRUD-Funktion auf, um die Priorität eines Issues in der Datenbank zu aktualisieren.
    """
    # Aufrufen der CRUD-Funktion zum Aktualisieren der Priorität des Issues
    updated_issue = update_priority(issue_id, user_id, priority_name)

    if not updated_issue:
        raise HTTPException(status_code=400, detail="Failed to update priority")

    return updated_issue
