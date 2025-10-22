from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import List, Optional
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactRead


class ContactService:

    @staticmethod
    def create_contact(session: Session, contact_data: ContactCreate) -> ContactRead:
        contact = Contact(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message,
            created_at=datetime.now(timezone.utc)
        )
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return ContactRead.from_orm(contact)

    
    @staticmethod
    def get_all_contacts(session: Session, unread_only: bool = False) -> List[ContactRead]:
        query = select(Contact)
        if unread_only:
            query = query.where(Contact.is_read == False)
        
        results = session.exec(query).all()
        return [ContactRead.from_orm(c) for c in results]

    
    @staticmethod
    def get_contact_by_id(session: Session, contact_id: int) -> Optional[ContactRead]:
        contact = session.get(Contact, contact_id)
        return ContactRead.from_orm(contact) if contact else None
