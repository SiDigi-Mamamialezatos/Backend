from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .module import Module
    from .attempt import Attempt


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    module_id: Mapped[str] = mapped_column(
        String, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # isi cerita/materi
    # array of {question, choices: [{text, isCorrect, feedback}]}
    questions: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    module: Mapped["Module"] = relationship(back_populates="materials")
    attempts: Mapped[List["Attempt"]] = relationship(
        back_populates="material", cascade="all, delete-orphan"
    )