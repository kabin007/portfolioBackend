from fastapi import APIRouter, Request, Depends
from sqlmodel import Session
from typing import List
from sqlalchemy import text

from app.database import get_db
from app.services.visitor import VisitorService
from app.schemas.visitor import VisitorRead, VisitorCreate

router = APIRouter(prefix="/visitor", tags=["Visitor"])


@router.get("/", response_model=List[VisitorRead])
def get_all_visitors(session: Session = Depends(get_db)):
    query = session.exec(text("SELECT * FROM visitor"))
    visitors = query.all()
    return [VisitorRead.from_orm(v) for v in visitors]


@router.post("/track", response_model=VisitorRead)
def track_visitor(request: Request, session: Session = Depends(get_db)):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip_address = forwarded.split(",")[0].strip()
        print("Ip address found in x forwarded for:", ip_address)

    else:
        ip_address = request.client.host

    visitor_create = VisitorCreate(
        ip_address=ip_address,
        user_agent=request.headers.get("user-agent", "")
    )

    visitor = VisitorService.create_or_update_visitor(session, visitor_create)
    print(visitor)
    return visitor
