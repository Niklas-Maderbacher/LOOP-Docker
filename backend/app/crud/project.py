from sqlalchemy.orm import Session
from app.db.models import UserAtProject

def update_user_role(db: Session, project_id: int, user_id: int, new_role_id: int):  
    user_at_project = db.query(UserAtProject).filter(
        UserAtProject.project_id == project_id,
        UserAtProject.user_id == user_id
    ).one()

    if not user_at_project:
        return None

    user_at_project.role_id = new_role_id
    db.commit()
    db.refresh(user_at_project)

    return user_at_project
        