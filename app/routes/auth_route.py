from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.schemas.auth_schema import RegisterUser, RegisterUserResponse, LoginUser, TokenResponse, ForgotPassword, ResetPassword
from app.services import auth_service
from app.database.db import get_db
from app.core.rate_limiter import limiter   

router = APIRouter()

@router.post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def user_register(request: Request, data: RegisterUser, db=Depends(get_db)):
    return auth_service.create_user(db, data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def user_login(request: Request, response: Response, data: LoginUser, db=Depends(get_db)):
    try:
        token_data = auth_service.login_user(db, data)
        if not token_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )
        
        response.set_cookie(
            key="refresh_token",
            value=token_data["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=10*24*60*60
        )

        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise e


@router.post("/refresh", status_code=status.HTTP_200_OK)
def create_new_access_token(request: Request, db=Depends(get_db)):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=401,
                detail="Refresh Token missing"
            )
        
        new_access_token = auth_service.new_access_token(db, refresh_token)
        if not new_access_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid Refresh token"
            )
        
        return new_access_token
    except Exception as e:
        raise e
    

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def forgot_password(request: Request, data: ForgotPassword, db=Depends(get_db)):
    return auth_service.forgot_password(db, data)


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(data: ResetPassword, db=Depends(get_db)):
    return auth_service.reset_password(db, data)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response, db=Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        auth_service.remove_refresh_token(db, refresh_token)

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {"message": "Logged out successfully"}