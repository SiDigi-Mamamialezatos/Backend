from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .attempt import Attempt
    from .user_badge import UserBadge
    from .chat import ChatSession
    from .auth import UserOAuth, RefreshToken


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    attempts: Mapped[List["Attempt"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    user_badges: Mapped[List["UserBadge"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    chat_sessions: Mapped[List["ChatSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    oauth_accounts: Mapped[List["UserOAuth"]] = relationship(
        "UserOAuth",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )