from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .user import User
    from .material import Material


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    material_id: Mapped[str] = mapped_column(
        String, ForeignKey("materials.id", ondelete="CASCADE"), nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="attempts")
    material: Mapped["Material"] = relationship(back_populates="attempts")