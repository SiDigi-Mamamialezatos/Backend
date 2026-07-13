from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBadgeBase(BaseModel):
    user_id: str
    badge_id: str


class UserBadgeCreate(UserBadgeBase):
    pass


class UserBadgeResponse(UserBadgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    earned_at: datetime