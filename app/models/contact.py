from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    message: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_read: bool = Field(default=False)

   