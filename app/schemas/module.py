from typing import Optional

from pydantic import BaseModel, ConfigDict


class ModuleBase(BaseModel):
    name: str  # e.g. "Bencana Alam", "Cyber Security", "Sosial"
    description: Optional[str] = None
    icon_url: Optional[str] = None
    order: int = 0


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    order: Optional[int] = None


class ModuleResponse(ModuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: str