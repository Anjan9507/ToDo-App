from fastapi import APIRouter, Depends, status
from app.schemas.auth_schema import RegisterUser, RegisterUserResponse
from app.services import auth_service
from app.database.db import get_db

router = APIRouter()

@router.post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterUser, db=Depends(get_db)):
    return auth_service.create_user(db, data)