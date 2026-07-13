from datetime import datetime
from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .user import User


class ChatRole(str, PyEnum):
    user = "user"
    assistant = "assistant"


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="chat_sessions")
    messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="chat_session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    chat_session_id: Mapped[str] = mapped_column(
        String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String, nullable=False)  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    chat_session: Mapped["ChatSession"] = relationship(back_populates="messages")