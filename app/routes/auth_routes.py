from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import TokenResponse, UserCreate, UserLogin, UserResponse, RefreshTokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.database.db import get_db
from app.models.user import User
from app.dependencies.dependency import get_current_user
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from datetime import timedelta
import os
from fastapi import HTTPException, status
from jose import JWTError, jwt


router=APIRouter(prefix='/auth', tags=["authentication"])


@router.post("/signup")
def signup(user_data: UserCreate, db= Depends(get_db)):
    """Register a new user"""
    auth_service = AuthService(db=db)
    return auth_service.register_user(user_data)


@router.post("/login")
def login(user_data: UserLogin, db= Depends(get_db)):
    """Login user and return JWT token"""
    auth_service = AuthService(db=db)
    return auth_service.authenticate_user(user_data)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )

@router.get("/users", response_model=list[UserResponse])
def get_all_users(db= Depends(get_db), user=Depends(get_current_user)):
    """Get all users"""
    user_service = UserService(db=db)
    return user_service.get_all_users()


@router.post("/tokens")
def get_tokens(request:Request, db:AsyncSession=Depends(get_db)):
    """
    Get refresh token and access tokens for user
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid refresh token")
    token = auth_header.split(" ")[1]

    auth_service = AuthService(db=db)
    tokens = auth_service._get_tokens(token)
    return tokens


@router.post('/forgot-password')
def forget_password(request: ForgotPasswordRequest , db:AsyncSession= Depends(get_db)):
    auth_service=AuthService(db=db)
    return auth_service._forgot_password(request.email)    


@router.post('/reset-password')
def reset_password(request: ResetPasswordRequest, db:AsyncSession= Depends(get_db)):
    auth_service=AuthService(db=db)
    return auth_service._reset_password(request.token, request.password)
