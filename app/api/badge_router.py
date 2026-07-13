from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db
from app.schemas.badge import BadgeCreate, BadgeUpdate, BadgeResponse
from app.services.badge_service import BadgeService

router = APIRouter(prefix="/badges", tags=["badges"])


@router.post("/", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
def create_badge(obj_in: BadgeCreate, db: Session = Depends(get_db)):
    return BadgeService(db).create(obj_in)


@router.get("/{badge_id}", response_model=BadgeResponse)
def get_badge(badge_id: str, db: Session = Depends(get_db)):
    return BadgeService(db).get_or_404(badge_id)


@router.get("/", response_model=List[BadgeResponse])
def list_badges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return BadgeService(db).list(skip=skip, limit=limit)


@router.patch("/{badge_id}", response_model=BadgeResponse)
def update_badge(badge_id: str, obj_in: BadgeUpdate, db: Session = Depends(get_db)):
    return BadgeService(db).update(badge_id, obj_in)


@router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(badge_id: str, db: Session = Depends(get_db)):
    BadgeService(db).delete(badge_id)