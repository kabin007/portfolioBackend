from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username:str
    email:str
    password:str

    model_config = ConfigDict(extra='forbid') 

class UserLogin(BaseModel):
    username:str
    password:str

    model_config = ConfigDict(extra='forbid') 
     
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    created_at:datetime

    model_config = {
        "from_attributes": True
    }


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token:str
    password:str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class RefreshTokenResponse(BaseModel):
    token:str
    jti:str
    expiry:str

