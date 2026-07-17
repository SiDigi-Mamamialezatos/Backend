from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: MaterialCreate) -> Material:
        data = obj_in.model_dump(mode="json")
        db_obj = Material(**data)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)

        return db_obj

    def get(self, material_id: str) -> Optional[Material]:
        return self.db.get(Material, material_id)

    def list_by_module(
        self,
        module_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Material]:
        return list(
            self.db.execute(
                select(Material)
                .where(Material.module_id == module_id)
                .order_by(Material.order)
                .offset(skip)
                .limit(limit)
            ).scalars()
        )

    def update(
        self,
        db_obj: Material,
        obj_in: MaterialUpdate,
    ) -> Material:
        data = obj_in.model_dump(
            exclude_unset=True,
            mode="json",
        )

        for field, value in data.items():
            setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)

        return db_obj

    def delete(self, db_obj: Material) -> None:
        self.db.delete(db_obj)
        self.db.commit()