from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatSessionBase(BaseModel):
    user_id: str


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionResponse(ChatSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime