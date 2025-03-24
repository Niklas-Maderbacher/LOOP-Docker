from pydantic import BaseModel

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueGet(BaseModel):
    name: str
    priority_id: int
    story_points: int
    responsible_user_id: int