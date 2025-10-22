from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VisitorBase(BaseModel):
    ip_address: str
    user_agent: str
    browser: Optional[str] = None
    os: Optional[str] = None
    device_type: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    org: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    visited_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class VisitorCreate(BaseModel):
    ip_address: str
    user_agent: str


class VisitorRead(VisitorBase):
    id: int
    visited_at: datetime  

    class Config:
        orm_mode = True 
