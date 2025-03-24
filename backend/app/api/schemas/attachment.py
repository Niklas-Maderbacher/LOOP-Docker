from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class AttachmentCreate(BaseModel):
    issue_id: int
    project_id: int
    filename: str