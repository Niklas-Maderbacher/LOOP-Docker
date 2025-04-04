from pydantic import BaseModel
from typing import Optional, Literal
from app.enums.issueType import Type
from app.enums.priority import Priority

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueCreate(BaseModel):
    name: str
    category: Type
    sprint_id: Optional[int]
    responsible_id: Optional[int]
    priority_id: Optional[Priority]
    description: str
    story_points: Optional[int]
    project_id: Optional[int]

