from typing import Optional

from pydantic import BaseModel, ConfigDict


class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    criteria: Optional[str] = None


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    criteria: Optional[str] = None


class BadgeResponse(BadgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: str