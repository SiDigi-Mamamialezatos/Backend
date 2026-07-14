from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None


class UserCreate(UserBase):
    """Request body for creating a user. Plain password in, never stored as-is."""
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Request body for partial updates. All fields optional."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Request body for login — plain JSON, no OAuth2 form."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Response body. Never includes hashed_password."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime