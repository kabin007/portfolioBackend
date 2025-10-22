from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select
from slugify import slugify 
from app.models.blog import BlogPost, Category
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostRead,
    CategoryCreate,
    CategoryRead
)


class CategoryService:

    @staticmethod
    def create_category(session: Session, category_data: CategoryCreate) -> CategoryRead:
        category = Category(**category_data.model_dump())
        session.add(category)
        session.commit()
        session.refresh(category)
        return CategoryRead.from_orm(category)

    @staticmethod
    def get_all_categories(session: Session) -> List[CategoryRead]:
        categories = session.exec(select(Category)).all()
        return [CategoryRead.from_orm(c) for c in categories]

    @staticmethod
    def get_category_by_id(session: Session, category_id: int) -> Optional[CategoryRead]:
        category = session.get(Category, category_id)
        return CategoryRead.from_orm(category) if category else None


class BlogService:

    @staticmethod
    def create_blog_post(session: Session, blog_data: BlogPostCreate) -> BlogPostRead:
        # Generate slug automatically if not provided
        slug = slugify(blog_data.slug or blog_data.title)

        post = BlogPost(
            title=blog_data.title,
            slug=slug,
            image=blog_data.image,
            content=blog_data.content,
            published=blog_data.published,
            category_id=blog_data.category_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(post)
        session.commit()
        session.refresh(post)
        return BlogPostRead.from_orm(post)

    @staticmethod
    def get_all_blog_posts(session: Session, published_only: bool = True) -> List[BlogPostRead]:
        query = select(BlogPost).order_by(BlogPost.created_at.desc())
        if published_only:
            query = query.where(BlogPost.published == True)
        posts = session.exec(query).all()
        return [BlogPostRead.from_orm(p) for p in posts]

    @staticmethod
    def get_blog_post_by_slug(session: Session, slug: str) -> Optional[BlogPostRead]:
        post = session.exec(select(BlogPost).where(BlogPost.slug == slug)).first()
        return BlogPostRead.from_orm(post) if post else None

    @staticmethod
    def update_blog_post(session: Session, post_id: int, update_data: BlogPostUpdate) -> Optional[BlogPostRead]:
        post = session.get(BlogPost, post_id)
        if not post:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(post, key, value)

        post.updated_at = datetime.now(timezone.utc)
        session.add(post)
        session.commit()
        session.refresh(post)
        return BlogPostRead.from_orm(post)

    @staticmethod
    def delete_blog_post(session: Session, post_id: int) -> bool:
        post = session.get(BlogPost, post_id)
        if not post:
            return False
        session.delete(post)
        session.commit()
        return True
