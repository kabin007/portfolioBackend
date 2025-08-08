import secrets
from datetime import datetime, timedelta
from app.models.user import ResetToken
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


def generate_secure_token(length: int = 32) -> str:
    # Generates a URL-safe secure random string token
    return secrets.token_urlsafe(length)


async def store_reset_token(db: AsyncSession, user_id: int, token: str, expires_in: int = 3600):
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    #delete existing tokens for user
    stmt = delete(ResetToken).where(ResetToken.user_id == user_id)
    await db.execute(stmt)

    reset_token = ResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(reset_token)
    await db.commit()


async def get_token_record(db:AsyncSession , token:str):

    #query the database for the token
    result= await db.execute(select(ResetToken).where(ResetToken.token==token))
    token_record=result.scalar_one_or_none()

    if not token_record:
        return {"No token record found with the given token"}

    return token_record

