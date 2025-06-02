from collections.abc import Generator
from sqlmodel import Session, create_engine, select

from app.config.config import settings
from app.api.schemas.user import UserCreateSuperuser  # Falls dein Schema anders liegt, bitte anpassen
from app.security.security import get_password_hash  # Falls du eine Hashing-Funktion hast

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

# SQLAlchemy
engine = create_engine(DATABASE_URL)

from app.db.models import Attachment, User, Sprint, UserAtProject, Project, Issue
from sqlmodel import SQLModel
# creating tables using SQLModel
# uncomment if you don't want to use alembic
SQLModel.metadata.create_all(engine)

def create_superuser_if_not_exists():
    with Session(engine) as session:
        superuser_exists = session.exec(select(User).where(User.is_admin == True)).first()
        if not superuser_exists:
            email = settings.FIRST_SUPERUSER  # Ändere die E-Mail nach Bedarf
            display_name = settings.FIRST_SUPERUSER_NAME
            password = settings.FIRST_SUPERUSER_PASSWORD  # Sicherstellen, dass das Passwort sicher ist
            hashed_password = get_password_hash(password)
            
            superuser_data = User(
                email=email,
                display_name=display_name,
                password=hashed_password,
                is_admin=True
            )

            session.add(superuser_data)
            session.commit()
            session.refresh(superuser_data)
            print(f"Superuser {email} wurde erfolgreich erstellt.")

# Superuser erstellen, falls nicht vorhanden
create_superuser_if_not_exists()
