from app.db.models import Role,  User, Project, UserAtProject
from sqlmodel import Session

def update_role(session: Session, user_id: int, project_id: int, new_role: str):

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User mit ID {user_id} existiert nicht.")
    
    project = session.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError(f"Project mit ID {project_id} existiert nicht.")
    
    role = session.query(Role).filter(Role.name == new_role).first()
    if not role:
        raise ValueError(f"Priority '{new_role}' existiert nicht.")

    user_project = session.query(UserAtProject).filter(
        UserAtProject.user_id == user_id,
        UserAtProject.project_id == project_id
    ).first()

    if not user_project:
        raise ValueError(f"User mit ID {user_id} ist nicht mit Project ID {project_id} verknüpft.")
    
    user_project.role_id = role.id
    session.commit()
    session.refresh(user_project)

    return user_project