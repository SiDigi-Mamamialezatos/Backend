from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from app.models.user import User
from app.schemas.attempt import AttemptCreate, AttemptUpdate, AttemptResponse
from app.services.attempt_service import AttemptService

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("/", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
def create_attempt(
    obj_in: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AttemptService(db).create(obj_in, current_user)


@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(attempt_id: str, db: Session = Depends(get_db)):
    return AttemptService(db).get_or_404(attempt_id)


@router.get("/user/{user_id}", response_model=List[AttemptResponse])
def list_attempts_by_user(
    user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return AttemptService(db).list_by_user(user_id, skip=skip, limit=limit)


@router.patch("/{attempt_id}", response_model=AttemptResponse)
def update_attempt(
    attempt_id: str,
    obj_in: AttemptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AttemptService(db).update(attempt_id, obj_in, current_user)


@router.post("/{attempt_id}/complete", response_model=AttemptResponse)
def complete_attempt(
    attempt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AttemptService(db).mark_completed(attempt_id, current_user)


@router.delete("/{attempt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attempt(
    attempt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    AttemptService(db).delete(attempt_id, current_user)