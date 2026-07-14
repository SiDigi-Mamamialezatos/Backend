# =============================================================
# app/models/auth.py
# SQLAlchemy 2.0 style - Fixed Data Type Mismatch
# =============================================================

import enum
import hashlib
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User


class OAuthProvider(enum.Enum):
    google = "google"


class UserOAuth(Base):
    __tablename__ = "user_oauth"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_id",
            name="uq_user_oauth_provider_provider_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # 🔄 CHANGED: Type updated from UUID to String to match users.id type
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    provider: Mapped[OAuthProvider] = mapped_column(
        SAEnum(OAuthProvider),
        nullable=False,
    )

    provider_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    provider_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    access_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user: Mapped["User"] = relationship(
        back_populates="oauth_accounts",
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # 🔄 CHANGED: Type updated from UUID to String to match users.id type
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    device_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens",
    )

    @staticmethod
    def hash_token(raw_token: str) -> str:
        """Always hash before storing or querying."""
        return hashlib.sha256(raw_token.encode()).hexdigest()