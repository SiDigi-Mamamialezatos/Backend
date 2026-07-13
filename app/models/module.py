from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, gen_uuid

if TYPE_CHECKING:
    from .material import Material


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)  # e.g. "Bencana Alam", "Cyber Security", "Sosial"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    materials: Mapped[List["Material"]] = relationship(
        back_populates="module", cascade="all, delete-orphan"
    )