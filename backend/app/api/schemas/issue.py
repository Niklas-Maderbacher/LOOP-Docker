from pydantic import BaseModel
from typing import Optional

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueCreate(BaseModel):
    name: str
    category_id: Optional[int]
    sprint_id: Optional[int]
    responsible_id: Optional[int]
    priority_id: Optional[int]
    description: str
    story_points: Optional[int]
    project_id: int
