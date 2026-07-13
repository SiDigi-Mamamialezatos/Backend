from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest
from app.services import auth_services
from app.db.sessions import get_db


router = APIRouter()

@router.get("/")
def auth():
    return{"message": "auth works!"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, session: Session = Depends(get_db)):
    return auth_services.register(session, payload)