from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.services.jwt import verify_access_token
from app.models.user import User
from app.database.db import get_db
from app.schemas.user_schema import UserResponse
from sqlalchemy import select



security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ) -> UserResponse:


        #Get current authenticated user from JWT token

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            token = credentials.credentials
            payload = verify_access_token(token)

            if payload is None:
                raise credentials_exception

            username = payload.get("username")
            user_id = payload.get("user_id")

            if username is None or user_id is None:
                raise credentials_exception

        except Exception:
            raise credentials_exception

        # Get user from database
        result = db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
