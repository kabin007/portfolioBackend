from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }



class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class BlogPostBase(BaseModel):
    title: str
    slug: str
    image: Optional[str] = None
    content: str
    published: bool = True

    model_config = {
        "from_attributes": True
    }


class BlogPostCreate(BlogPostBase):
    category_id: Optional[int] = None


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    category_id: Optional[int] = None


class BlogPostRead(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryRead] = None

    class Config:
        orm_mode = True
