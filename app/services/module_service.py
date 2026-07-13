from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.module import Module
from app.repositories.module_repo import ModuleRepository
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModuleRepository(db)

    def create(self, obj_in: ModuleCreate) -> Module:
        return self.repo.create(obj_in)

    def get_or_404(self, module_id: str) -> Module:
        module = self.repo.get(module_id)
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Module not found"
            )
        return module

    def list(self, skip: int = 0, limit: int = 100) -> List[Module]:
        return self.repo.list(skip=skip, limit=limit)

    def update(self, module_id: str, obj_in: ModuleUpdate) -> Module:
        module = self.get_or_404(module_id)
        return self.repo.update(module, obj_in)

    def delete(self, module_id: str) -> None:
        module = self.get_or_404(module_id)
        self.repo.delete(module)