from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum


class RefreshToken(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    created_at:datetime=Field(default_factory=datetime.utcnow)
    jti:str=Field(nullable=False, unique=True)
    expires_at:datetime=Field(nullable=False)
    revoked:bool=Field(default=False)

    #foreign key relationship with the user
    user_id:int=Field(foreign_key="user.id", nullable=False)
    user:Optional["User"]=Relationship(back_populates="refresh_tokens")



class ResetToken(SQLModel, table=True):
    id:Optional[int] =Field(default=None, primary_key=True)
    token:str= Field(nullable=False, unique=True)
    expires_at:datetime= Field(nullable=False)

    # Foreign key relationship with the user
    user_id:int =Field(foreign_key="user.id", nullable=False)
    user:Optional["User"]=Relationship(back_populates="reset_tokens")



class User(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    fullname: Optional[str] = Field(default=None , nullable=True)
    username:str=Field(index=True, nullable=False, unique=True)
    email:str=Field(index=True, nullable=False, unique=True)
    hashed_password:str=Field(nullable=False)
    created_at:datetime=Field(default_factory=datetime.utcnow)

    #refresh tokens
    refresh_tokens:List["RefreshToken"]=Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade":"all, delete-orphan"}
    )

    #reset tokens
    reset_tokens:List["ResetToken"]=Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade":"all, delete-orphan"}
    )



