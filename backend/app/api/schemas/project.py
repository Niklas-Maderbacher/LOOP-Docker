from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ProjectCreate(BaseModel):
    name: str = Field(max_length=100, nullable=False)
    start_date: Optional[date] = Field(default=None)
    github_token: Optional[str] = Field(default=None, max_length=70)
