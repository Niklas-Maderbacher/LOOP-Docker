from sqlalchemy.orm import Session
from app.db.models import Sprint, UserAtProject
from app.enums.role import Role
from app.api.schemas.sprint import SprintCreate

## Loop-101 Thomas Sommerauer
def create_sprint(db: Session, user_id: int, sprint_data: SprintCreate):
    # Check if user is Admin
    from app.db.models import User
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception("User not found")

    is_admin = user.is_admin

    # Check if user is Product Owner for this project
    user_at_project = db.query(UserAtProject).filter(
        UserAtProject.user_id == user_id,
        UserAtProject.project_id == sprint_data.project_id
    ).first()

    is_po = user_at_project and user_at_project.role == Role.PRODUCTOWNER

    if not (is_admin or is_po):
        raise PermissionError("Unauthorized")

    # Check if there is an active sprint (no end_date yet)
    active_sprint = db.query(Sprint).filter(
        Sprint.project_id == sprint_data.project_id,
        Sprint.end_date == None
    ).first()

    if active_sprint:
        raise ValueError("There is already an active sprint.")

    # Create sprint
    new_sprint = Sprint(
        name=sprint_data.name,
        project_id=sprint_data.project_id,
        start_date=sprint_data.start_date,
        end_date=sprint_data.end_date,
        goal=sprint_data.goal
    )
    db.add(new_sprint)
    db.commit()
    db.refresh(new_sprint)

    return new_sprint
#############################################