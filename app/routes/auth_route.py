from fastapi import APIRouter, Depends, status
from app.schemas.auth_schema import RegisterUser, RegisterUserResponse, LoginUser, TokenResponse
from app.services import auth_service
from app.database.db import get_db

router = APIRouter()

@router.post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
def user_register(data: RegisterUser, db=Depends(get_db)):
    return auth_service.create_user(db, data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def user_login(data: LoginUser, db=Depends(get_db)):
    return auth_service.login_user(db, data)
