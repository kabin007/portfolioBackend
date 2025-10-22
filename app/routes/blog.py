from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database import get_db
from app.services.blog import BlogService, CategoryService
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostRead,
    BlogPostUpdate,
    CategoryCreate,
    CategoryRead
)

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.post("/categories/", response_model=CategoryRead)
def create_category(data: CategoryCreate, session: Session = Depends(get_db)):
    return CategoryService.create_category(session, data)


@router.get("/categories/", response_model=List[CategoryRead])
def list_categories(session: Session = Depends(get_db)):
    return CategoryService.get_all_categories(session)

@router.post("/posts/", response_model=BlogPostRead)
def create_blog_post(data: BlogPostCreate, session: Session = Depends(get_db)):
    return BlogService.create_blog_post(session, data)


@router.get("/posts/", response_model=List[BlogPostRead])
def list_blog_posts(session: Session = Depends(get_db)):
    return BlogService.get_all_blog_posts(session)


@router.get("/posts/{slug}", response_model=BlogPostRead)
def get_blog_post(slug: str, session: Session = Depends(get_db)):
    post = BlogService.get_blog_post_by_slug(session, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/posts/{post_id}", response_model=BlogPostRead)
def update_blog_post(post_id: int, data: BlogPostUpdate, session: Session = Depends(get_db)):
    post = BlogService.update_blog_post(session, post_id, data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/posts/{post_id}")
def delete_blog_post(post_id: int, session: Session = Depends(get_db)):
    success = BlogService.delete_blog_post(session, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
