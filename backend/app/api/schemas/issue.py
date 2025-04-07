from sqlmodel import Field
from typing import Optional
from pydantic import BaseModel

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class GetIssue(BaseModel):
    project_id: int
    name: str
    priority_id: Optional[int] = Field(default=None)
    story_points: Optional[int] = Field(default=None)
    responsible_user_id: Optional[int] = Field(default=None)