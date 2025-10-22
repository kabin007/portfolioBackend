from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    name: str
    email: EmailStr
    message: str

    model_config = {
        "from_attributes": True
    }



class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True
