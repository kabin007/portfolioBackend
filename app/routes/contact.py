from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database import get_db
from app.services.contact import ContactService
from app.schemas.contact import ContactCreate, ContactRead

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactRead)
def create_contact(contact_data: ContactCreate, session: Session = Depends(get_db)):
    """Create a new contact message"""
    return ContactService.create_contact(session, contact_data)


@router.get("/", response_model=List[ContactRead])
def list_contacts(unread_only: bool = False, session: Session = Depends(get_db)):
    return ContactService.get_all_contacts(session, unread_only)


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, session: Session = Depends(get_db)):
    contact = ContactService.get_contact_by_id(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

