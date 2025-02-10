from pydantic import BaseModel

class StoryPointUpdate(BaseModel):
    new_story_point_value: int