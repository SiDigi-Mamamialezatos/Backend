from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ChatMessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatMessageBase(BaseModel):
    chat_session_id: str
    role: ChatMessageRole
    content: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageWithBotCreate(BaseModel):
    """Post a user message to an existing session and ask the bot to reply.

    This lives alongside ChatMessageCreate so plain message persistence still works.
    """

    chat_session_id: str
    module_slug: str
    content: str


class ChatMessageResponse(ChatMessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime