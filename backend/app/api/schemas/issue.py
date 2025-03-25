from pydantic import BaseModel
from typing import Optional, Literal
from app.enums.issueType import Type

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueCreate(BaseModel):
    name: str
    category_id: Type
    sprint_id: Optional[int]
    responsible_id: Optional[int]
    priority_id: Optional[int]
    description: str
    story_points: Optional[int]
    project_id: int

