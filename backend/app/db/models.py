import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel  
from sqlalchemy import Numeric, TIMESTAMP
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import EmailStr

class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)

    users_at_project: List["UserAtProject"] = Relationship(back_populates="role")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=320)
    display_name: str = Field(max_length=100, nullable=False)
    password: str = Field(max_length=30, nullable=False)
    microsoft_account: bool = Field(default=False)
    archived: Optional[str] = Field(default=None)
    last_active: Optional[str] = Field(default=None)
    is_email_verified: bool = Field(default=False)
    mobile_number: Optional[str] = Field(default=None, max_length=20)

    user_at_projects: List["UserAtProject"] = Relationship(back_populates="user")
    issues_created: List["Issue"] = Relationship(back_populates="creator")
    issues_responsible: List["Issue"] = Relationship(back_populates="responsible_user")

class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    archived_at: Optional[str] = Field(default=None)
    github_token: Optional[str] = Field(default=None, max_length=70)

    sprints: List["Sprint"] = Relationship(back_populates="project")
    issues: List["Issue"] = Relationship(back_populates="project")
    user_at_projects: List["UserAtProject"] = Relationship(back_populates="project")

class UserAtProject(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id")

    user: "User" = Relationship(back_populates="user_at_projects")
    project: "Project" = Relationship(back_populates="user_at_projects")
    role: "Role" = Relationship(back_populates="users_at_project")

class Sprint(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    project_id: int = Field(foreign_key="project.id")
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)

    project: "Project" = Relationship(back_populates="sprints")
    issues: List["Issue"] = Relationship(back_populates="sprint")

class Priority(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)

    issues: List["Issue"] = Relationship(back_populates="priority")

class State(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)

    issues: List["Issue"] = Relationship(back_populates="state")

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)

    issues: List["Issue"] = Relationship(back_populates="category")

class Attachment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    issue_id: int = Field(foreign_key="issue.id")
    link: str = Field(nullable=False)

    issue: "Issue" = Relationship(back_populates="attachments")

class Issue(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    category_id: Optional[int] = Field(foreign_key="category.id")
    sprint_id: Optional[int] = Field(foreign_key="sprint.id")
    state_id: Optional[int] = Field(foreign_key="state.id")
    creator_id: Optional[int] = Field(foreign_key="user.id")
    responsible_user_id: Optional[int] = Field(foreign_key="user.id")
    priority_id: Optional[int] = Field(foreign_key="priority.id")
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

    category: "Category" = Relationship(back_populates="issues")
    sprint: "Sprint" = Relationship(back_populates="issues")
    state: "State" = Relationship(back_populates="issues")
    creator: "User" = Relationship(back_populates="issues_created")
    responsible_user: "User" = Relationship(back_populates="issues_responsible")
    priority: "Priority" = Relationship(back_populates="issues")
    project: "Project" = Relationship(back_populates="issues")
    attachments: List["Attachment"] = Relationship(back_populates="issue")

##########################################################
# export PYTHONPATH=$PWD
# alembic upgrade head
# alembic revision --autogenerate -m "Add mit neue tabelle6"
