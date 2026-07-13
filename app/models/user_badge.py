from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .user import User
    from .badge import Badge


class UserBadge(Base):
    __tablename__ = "user_badges"
    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    badge_id: Mapped[str] = mapped_column(
        String, ForeignKey("badges.id", ondelete="CASCADE"), nullable=False
    )
    earned_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="user_badges")
    badge: Mapped["Badge"] = relationship(back_populates="user_badges")