from pydantic import BaseModel
from typing import Optional

class AttachmentCreate(BaseModel):
    issue_id: int
    link: str  # This will store the file URL/path
