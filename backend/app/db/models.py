from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column
from typing import List, Optional
from pydantic import EmailStr
from app.db.session import engine
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import ENUM
from app.enums.role import Role
from app.enums.issueType import Type
from app.enums.state import State
from app.enums.priority import Priority


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=320)
    display_name: str = Field(max_length=100, nullable=False)
    password: str = Field(max_length=100, nullable=False)
    microsoft_account: bool = Field(default=False)
    archived: Optional[str] = Field(default=None)
    last_active: Optional[str] = Field(default=None)
    is_email_verified: bool = Field(default=False)
    mobile_number: Optional[str] = Field(default=None, max_length=20)
    is_admin: bool = Field(default=False)

class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    key: str = Field(max_length=10, unique=True, nullable=False)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    archived_at: Optional[str] = Field(default=None)
    github_token: Optional[str] = Field(default=None, max_length=70)

class UserAtProject(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    role: Role = Field(sa_column=Column(ENUM(Role, name="role_enum", create_type=True), nullable=False, default=Role.USER))

class Sprint(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    project_id: int = Field(foreign_key="project.id")
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)

class Priority(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)

class State(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)

class Attachment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    issue_id: int = Field(foreign_key="issue.id")
    project_id: int = Field(foreign_key="project.id")
    filename: str = Field(nullable=False)

class Issue(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    category: Type = Field(sa_column=Column(ENUM(Type, name="category_enum", create_type=True), nullable=False))
    sprint_id: Optional[int] = Field(foreign_key="sprint.id")
    state: Optional[State] = Field(sa_column=Column(ENUM(State, name="state_enum", create_type=True), nullable=True))
    creator_id: Optional[int] = Field(foreign_key="user.id")
    responsible_user_id: Optional[int] = Field(foreign_key="user.id")
    priority: Priority = Field(sa_column=Column(ENUM(Priority, name="priority_enum", create_type=True), nullable=True))
    description: Optional[str] = Field(default=None)
    repository_link: Optional[str] = Field(default=None)
    story_points: Optional[int] = Field(default=None)
    report_time: Optional[str] = Field(default=None)
    version: Optional[int] = Field(default=None)
    updater_id: Optional[int] = Field(foreign_key="user.id")
    project_id: int = Field(foreign_key="project.id")
    updated_at: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    backlog_order_number: Optional[int] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None)
    finisher_id: Optional[int] = Field(foreign_key="user.id")
    parent_issue_id: Optional[int] = Field(foreign_key="issue.id")
