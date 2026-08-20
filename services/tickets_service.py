from sqlalchemy.orm import Session
from repositories import ticket_repository
from schemas.tickets import TicketUpdate, TicketCreate
from database.models import Tickets
from fastapi import HTTPException, status

def get_all_tickets(db: Session):
    ticket = ticket_repository.get_all_tickets(db)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No tickets found")
    return ticket

def get_ticket(db: Session, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No ticket with ID found")
    return ticket

def create_ticket(db: Session, newTicket: TicketCreate):
    ticket = newTicket.model_dump()
    db_ticket = Tickets(**ticket)

    return ticket_repository.create_ticket(db, db_ticket)

def update_ticket(db: Session, updateTicket: TicketUpdate, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Ticket with ID not found")

    db_ticket = updateTicket.model_dump(exclude_unset=True)
    for key, value in db_ticket.items():
        setattr(ticket, key, value)

    return ticket_repository.update_ticket(db, ticket)

def delete_ticket(db: Session, ticket_id: int):
    return ticket_repository.delete_ticket(db, ticket_id)