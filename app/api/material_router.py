from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db
from app.schemas.material import MaterialCreate, MaterialUpdate, MaterialResponse
from app.services.material_service import MaterialService

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(obj_in: MaterialCreate, db: Session = Depends(get_db)):
    return MaterialService(db).create(obj_in)


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: str, db: Session = Depends(get_db)):
    return MaterialService(db).get_or_404(material_id)


@router.get("/module/{module_id}", response_model=List[MaterialResponse])
def list_materials_by_module(
    module_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return MaterialService(db).list_by_module(module_id, skip=skip, limit=limit)


@router.patch("/{material_id}", response_model=MaterialResponse)
def update_material(material_id: str, obj_in: MaterialUpdate, db: Session = Depends(get_db)):
    return MaterialService(db).update(material_id, obj_in)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: str, db: Session = Depends(get_db)):
    MaterialService(db).delete(material_id)