from pydantic import BaseModel
from typing import Optional
from app.enums.issueType import Type
from app.enums.state import State

from app.enums.priority import Priority

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueCreate(BaseModel):
    name: str
    category: Type
    state: State
    sprint_id: Optional[int] = None
    responsible_user_id: Optional[int] = None
    priority: Optional[Priority] = None
    description: str
    story_points: Optional[int] = None
    project_id: Optional[int] = None