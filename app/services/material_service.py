from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.material import Material
from app.repositories.material_repo import MaterialRepository
from app.repositories.module_repo import ModuleRepository
from app.schemas.material import MaterialCreate, MaterialUpdate


class MaterialService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MaterialRepository(db)
        self.module_repo = ModuleRepository(db)

    def create(self, obj_in: MaterialCreate) -> Material:
        if not self.module_repo.get(obj_in.module_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Module not found"
            )
        return self.repo.create(obj_in)

    def get_or_404(self, material_id: str) -> Material:
        material = self.repo.get(material_id)
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material not found"
            )
        return material

    def list_by_module(self, module_id: str, skip: int = 0, limit: int = 100) -> List[Material]:
        if not self.module_repo.get(module_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Module not found"
            )
        return self.repo.list_by_module(module_id, skip=skip, limit=limit)

    def update(self, material_id: str, obj_in: MaterialUpdate) -> Material:
        material = self.get_or_404(material_id)
        if obj_in.module_id and not self.module_repo.get(obj_in.module_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Module not found"
            )
        return self.repo.update(material, obj_in)

    def delete(self, material_id: str) -> None:
        material = self.get_or_404(material_id)
        self.repo.delete(material)