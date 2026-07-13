from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttemptBase(BaseModel):
    user_id: str
    material_id: str
    is_completed: bool = False
    completed_at: Optional[datetime] = None


class AttemptCreate(BaseModel):
    user_id: str
    material_id: str


class AttemptUpdate(BaseModel):
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class AttemptResponse(AttemptBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime