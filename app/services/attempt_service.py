from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.user import User
from app.repositories.attempt_repo import AttemptRepository
from app.repositories.material_repo import MaterialRepository
from app.schemas.attempt import AttemptCreate, AttemptUpdate


class AttemptService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AttemptRepository(db)
        self.material_repo = MaterialRepository(db)

    def create(self, obj_in: AttemptCreate, current_user: User) -> Attempt:
        if obj_in.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create an attempt for another user",
            )
        if not self.material_repo.get(obj_in.material_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material not found"
            )
        return self.repo.create(obj_in)

    def get_or_404(self, attempt_id: str) -> Attempt:
        attempt = self.repo.get(attempt_id)
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found"
            )
        return attempt

    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Attempt]:
        return self.repo.list_by_user(user_id, skip=skip, limit=limit)

    def update(self, attempt_id: str, obj_in: AttemptUpdate, current_user: User) -> Attempt:
        attempt = self._get_owned_or_404(attempt_id, current_user)
        return self.repo.update(attempt, obj_in)

    def mark_completed(self, attempt_id: str, current_user: User) -> Attempt:
        attempt = self._get_owned_or_404(attempt_id, current_user)
        return self.repo.mark_completed(attempt)

    def delete(self, attempt_id: str, current_user: User) -> None:
        attempt = self._get_owned_or_404(attempt_id, current_user)
        self.repo.delete(attempt)

    def _get_owned_or_404(self, attempt_id: str, current_user: User) -> Attempt:
        attempt = self.get_or_404(attempt_id)
        if attempt.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to modify this attempt",
            )
        return attempt