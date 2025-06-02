from pydantic import BaseModel
from typing import Optional

## Loop-101 Thomas Sommerauer
class SprintCreate(BaseModel):
    name: str
    project_id: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    goal: Optional[str] = None
########################