from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=100, nullable=False)
    display_name: str = Field(max_length=100, nullable=False)
    password: str = Field(max_length=100, nullable=False)
    microsoft_account: bool = Field(default=False)
    archived: Optional[str] = Field(default=None)
    last_active: Optional[str] = Field(default=None)
    is_email_verified: bool = Field(default=False)
    mobile_number: Optional[str] = Field(default=None, max_length=20)
    is_admin: bool = Field(default=False)
