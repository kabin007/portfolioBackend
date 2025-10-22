from fastapi import Depends
from app.models.user import User
from app.schemas.user_schema import UserResponse
from typing import List
from sqlalchemy import select, update
from app.database import get_db


class UserService:
    def __init__(self, db=Depends(get_db)):
            self.db = db
    
    def get_all_users(self) -> List[UserResponse]:
        """Get all users"""
        result = self.db.execute(select(User))
        users = result.scalars().all()

        return [UserResponse.from_orm(user) for user in users]
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        result= self.db.execute(select(User).where(User.id==user_id))
        user = result.scalar_one_or_none()
        return user
    
    def get_user_by_username(self, username: str) -> User:
        """Get user by username"""
        result= self.db.execute(select(User).where(User.username==username))
        user = result.scalar_one_or_none()
        return user
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        result= self.db.execute(select(User).where(User.email==email))
        user = result.scalar_one_or_none()
        return user


    def update_user_password(self, user_id: int, new_hashed_password: str):
        """Update the user password"""
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(hashed_password=new_hashed_password)
        )
        self.db.execute(stmt)
        self.db.commit()
