import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class TemplateShowcase(SQLModel):
    template: str = Field(default=None, max_length=255)
