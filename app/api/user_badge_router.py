from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db
from app.schemas.user_badge import UserBadgeCreate, UserBadgeResponse
from app.services.user_badge_service import UserBadgeService

router = APIRouter(prefix="/user-badges", tags=["user-badges"])


@router.post("/", response_model=UserBadgeResponse, status_code=status.HTTP_201_CREATED)
def award_badge(obj_in: UserBadgeCreate, db: Session = Depends(get_db)):
    return UserBadgeService(db).award(obj_in)


@router.get("/{user_badge_id}", response_model=UserBadgeResponse)
def get_user_badge(user_badge_id: str, db: Session = Depends(get_db)):
    return UserBadgeService(db).get_or_404(user_badge_id)


@router.get("/user/{user_id}", response_model=List[UserBadgeResponse])
def list_user_badges(user_id: str, db: Session = Depends(get_db)):
    return UserBadgeService(db).list_by_user(user_id)


@router.delete("/{user_badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_badge(user_badge_id: str, db: Session = Depends(get_db)):
    UserBadgeService(db).revoke(user_badge_id)