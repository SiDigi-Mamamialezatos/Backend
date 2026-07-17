from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Choice(BaseModel):
    text: str
    isCorrect: bool
    feedback: Optional[str] = None


class Question(BaseModel):
    question: str
    choices: List[Choice]


from typing import Any, Optional, List

class MaterialBase(BaseModel):
    module_id: str
    title: str
    narrative: Optional[List[str]] = None
    questions: Optional[List[Any]] = None
    order: int = 0


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    module_id: Optional[str] = None
    title: Optional[str] = None
    narrative: Optional[List[str]] = None
    questions: Optional[List[Question]] = None
    order: Optional[int] = None


class MaterialResponse(MaterialBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime