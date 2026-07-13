from app.db.base import Base
from sqlalchemy import String, Boolean, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship 
import uuid

class User(Base):
    __tablename__="users"

    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    email:Mapped[str]=mapped_column(String(255), unique=True)
    hashed_password:Mapped[str]=mapped_column(String(20))
    username:Mapped[str]=mapped_column(String(255))
