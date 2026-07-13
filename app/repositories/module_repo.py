from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: ModuleCreate) -> Module:
        db_obj = Module(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, module_id: str) -> Optional[Module]:
        return self.db.get(Module, module_id)

    def list(self, skip: int = 0, limit: int = 100) -> List[Module]:
        return list(
            self.db.execute(
                select(Module).order_by(Module.order).offset(skip).limit(limit)
            ).scalars()
        )

    def update(self, db_obj: Module, obj_in: ModuleUpdate) -> Module:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Module) -> None:
        self.db.delete(db_obj)
        self.db.commit()