from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .user_badge import UserBadge


class Badge(Base):
    __tablename__ = "badges"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    criteria: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user_badges: Mapped[List["UserBadge"]] = relationship(
        back_populates="badge", cascade="all, delete-orphan"
    )