from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    description: Optional[str] = Field(default=None)

    # one-to-many relationship
    posts: List["BlogPost"] = Relationship(back_populates="category")


class BlogPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    slug: str = Field(nullable=False, unique=True)
    image: str = Field(nullable=True, default=None)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    published: bool = Field(default=True)

    category_id: Optional[int] = Field(foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="posts")

