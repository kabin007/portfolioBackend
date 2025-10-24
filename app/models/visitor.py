from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Visitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_address: str = Field(nullable=False, index=True)
    user_agent: Optional[str] = Field(default=None)
    visited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    browser: Optional[str] = Field(default=None)
    os: Optional[str] = Field(default=None)
    device_type: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    no_of_visits: int = Field(default=1)
