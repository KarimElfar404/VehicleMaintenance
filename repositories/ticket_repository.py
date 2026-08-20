from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Tickets
from schemas.tickets import TicketCreate, TicketUpdate

def get_all_tickets(db: Session):
    statement = select(Tickets)
    return db.execute(statement).scalars().all()

def get_ticket(db: Session, ticket_id: int):
    return db.get(Tickets, ticket_id)

def create_ticket(db: Session, newTicket: TicketCreate):
    db.add(newTicket)
    db.commit()
    db.refresh(newTicket)
    return newTicket

def update_ticket(db: Session, updateTicket: TicketUpdate):
    db.commit()
    db.refresh(updateTicket)
    return updateTicket

def delete_ticket(db: Session, ticket_id: int):
    db.delete(ticket_id)
    db.commit()
    return None
