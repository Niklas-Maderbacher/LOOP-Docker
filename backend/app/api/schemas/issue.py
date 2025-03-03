from pydantic import BaseModel

class StoryPointUpdate(BaseModel):
    new_story_point_value: int

class IssueCreate(BaseModel):
    name: str
    project_id: int
    attachments: list[str]

class IssueUpdate(BaseModel):
    name: str
    attachments: list[str]

class IssueResponse(BaseModel):
    id: int
    name: str
    project_id: int