from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse
from app.services.module_service import ModuleService

router = APIRouter(prefix="/modules", tags=["modules"])


@router.post("/", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(obj_in: ModuleCreate, db: Session = Depends(get_db)):
    return ModuleService(db).create(obj_in)


@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(module_id: str, db: Session = Depends(get_db)):
    return ModuleService(db).get_or_404(module_id)


@router.get("/", response_model=List[ModuleResponse])
def list_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ModuleService(db).list(skip=skip, limit=limit)


@router.patch("/{module_id}", response_model=ModuleResponse)
def update_module(module_id: str, obj_in: ModuleUpdate, db: Session = Depends(get_db)):
    return ModuleService(db).update(module_id, obj_in)


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(module_id: str, db: Session = Depends(get_db)):
    ModuleService(db).delete(module_id)