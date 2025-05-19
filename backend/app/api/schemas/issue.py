from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from typing import Optional, Literal
from app.enums.issueType import Type
from app.enums.priority import Priority

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

# LOOP-124
class IssueUpdate(BaseModel):
    name: Optional[str] = Field(max_length=100, nullable=False)
    category_id: Optional[int] = Field(foreign_key="category.id")
    sprint_id: Optional[int] = Field(foreign_key="sprint.id")
    state_id: Optional[int] = Field(foreign_key="state.id")
    responsible_user_id: Optional[int] = Field(foreign_key="user.id")
    priority_id: Optional[int] = Field(foreign_key="priority.id")
    description: Optional[str] = Field(default=None)
    repository_link: Optional[str] = Field(default=None)
    story_points: Optional[int] = Field(default=None)
    project_id: int = Field(foreign_key="project.id")
    backlog_order_number: Optional[int] = Field(default=None)
    parent_issue_id: Optional[int] = Field(foreign_key="issue.id")


class IssueCreate(BaseModel):
    name: str
    category: Type
    sprint_id: Optional[int]
    responsible_id: Optional[int]
    priority_id: Optional[Priority]
    description: str
    story_points: Optional[int]
    project_id: Optional[int]

