from sqlalchemy.orm import Session
from repositories import ticket_repository, maintenance_history_repository
from schemas.tickets import TicketUpdate, TicketCreate, TicketStatus
from database.models import Tickets, MaintenanceHistory
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

def create_ticket(db: Session, newTicket: TicketCreate, vehicle_id: int):
    if not vehicle_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Profile does not have an assigned vehicle.")
    ticket = newTicket.model_dump()
    db_ticket = Tickets(**ticket, vehicle_id=vehicle_id)

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

def update_ticket_status(db: Session, ticket_id: int, new_status: TicketStatus):
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Ticket with ID is not found")
    if new_status == TicketStatus.CLOSED and ticket.ticket_status != TicketStatus.CLOSED:
        
        category_name = ticket.maintenance_category.maintenance_category_name if ticket.maintenance_category else "N/A"
        subcategory_name = ticket.maintenance_subcategory.maintenance_subcategory_name if ticket.maintenance_subcategory else "N/A"

        history_entry = MaintenanceHistory(
            vehicle_id=ticket.vehicle_id,
            ticket_id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            maintenance_category_name=category_name,
            maintenance_subcategory_name=subcategory_name,
            price=ticket.price
        )
        maintenance_history_repository.maintenance_entry_history(db, history_entry)
    ticket.ticket_status = new_status
    return ticket_repository.update_ticket_status(db, ticket)