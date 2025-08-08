from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from app.models.user import User, RefreshToken
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.jwt import (
    get_password_hash,
    create_access_token,
    verify_password,
    create_refresh_token,
)
from datetime import timedelta
import os
from sqlalchemy import select
from jose import JWTError, jwt
from datetime import datetime
from app.config import settings
from .user_service import UserService
from app.database.db import get_db
from app.utils.email import send_email
from app.utils.reset_password import generate_secure_token, get_token_record, store_reset_token
import logging
import traceback


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: UserCreate) -> dict:
        """Register a new user and return token response"""

       # Check if username already exists
        result = await self.db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Check if email already exists
        result = await self.db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        
        '''
        So, we have to enforce the strong password enforcement here, as soon as the user signs up or registers
        so we have to create a function that has the following signature


        name: enforce_password or something

        Args:
            -user sent password
        
        Returns:
            -
        '''
        
        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        # Create access token
        access_token = self._create_user_token(db_user)
        
        return {
           "token":{
                "access_token":access_token,
                "token_type":"bearer"
           }
        }

    
    async def authenticate_user(self, user_data: UserLogin) -> dict:
        """Authenticate user and return token response"""
        
        # Find user by username
        result= await self.db.execute(select(User).where(User.username==user_data.username))
        user=result.scalar_one_or_none()

        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = self._create_user_token(user)

        # create refresh token
        refresh_token, jti, expires = create_refresh_token(user.id)

        #save the refresh token information in the database for the future purpose
        refresh=RefreshToken(
            jti=jti,
            expires_at=expires,
            user_id=user.id
        )

        self.db.add(refresh)
        await self.db.commit()
        # await self.db.refresh(refresh)

        return {
            "tokens": {
                "access": {
                    "access_token": access_token,
                    "token_type": "bearer",
                },
                "refresh": {
                    "refresh_token": refresh_token,
                    "jti": jti,
                    "expiry": expires,
                },
            },
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        }


    def _create_user_token(self, user: User) -> str:
        """Create JWT token for user"""
        access_token_expires =settings.access_token_expire_minutes
        return create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
            },
            expires_delta=access_token_expires,
        )

    
    def _create_refresh_token(self, user_id: int):
        """
        Create refresh token for the user
        """
        refresh_token, jti, expiry = create_refresh_token(user_id)
        return refresh_token, jti, expiry

    
    async def _get_tokens(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
            user_id = int(payload.get("sub"))
            jti = payload.get("jti")
            exp = payload.get("exp")
        
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        #query and check the refresh token in the database if it is available
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        stored_token = result.scalar_one_or_none()

        if not stored_token or stored_token.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked or not found")

        # Revoke old token
        stored_token.revoked = True
        await self.db.commit()

        #query the database with the user_id
        result= await self.db.execute(select(User).where(User.id==user_id))
        user = result.scalar_one_or_none()

        user_dict={
            "id":user.id,
            "username":user.username,
            "email":user.email
        }

        # Issue new tokens
        new_refresh_token, new_jti, new_exp = create_refresh_token(user_id)
        access_token = create_access_token(user_dict)

        # Store new refresh token in DB
        db_refresh = RefreshToken(
            jti=new_jti,
            expires_at=new_exp,
            user=user
        )

        self.db.add(db_refresh)
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
        }


    async def _forgot_password(self, email: str):

        try:
            user_service = UserService(db=self.db)
            user = await user_service.get_user_by_email(email)  

            if not user:
                return {"message": "If that email exists, a reset link has been sent."}

            token = generate_secure_token()


            await store_reset_token(db=self.db, user_id=user.id, token=token, expires_in=3600)

            reset_link = f"https://frontend.com/reset-password?token={token}"
             
            #send email to the user
            await send_email(
                to=email,
                subject="Your Password Reset Link",
                body=f"Click here to reset your password: {reset_link}\nLink expires in 1 hour."
            )

            return {"message": "I have sent you the forget password link in your email"}

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Exception in _forgot_password: {e}")
            logger.error(traceback.format_exc())

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request."
            ) from e


    async def _reset_password(self, token: str, new_password: str):
        try:
            token_record = await get_token_record(self.db, token)
            if not token_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired token."
                )
            
            if token_record.expires_at < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token has expired. Please request a new password reset."
                )
            
            user_service=UserService(db=self.db)
            user = await user_service.get_user_by_id(token_record.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token user."
                )
            
            #hash the new password
            hashed_password = get_password_hash(new_password)
            
            #update the user's password
            await user_service.update_user_password(user.id, hashed_password) 
            
            return {"message": "Password successfully reset."}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Exception in _reset password: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            ) from e

