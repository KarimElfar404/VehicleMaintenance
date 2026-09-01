from sqlalchemy.orm import Session
from repositories import ticket_repository, maintenance_history_repository
from schemas.tickets import TicketUpdate, TicketCreate, TicketStatus
from database.models import Tickets, MaintenanceHistory, TicketItem, User
from fastapi import HTTPException, status
from datetime import date
from repositories import driver_user_repository

ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.OPEN: {
        TicketStatus.WAITING, # Reviewer asks for info
        TicketStatus.ACCEPTED, # Reviewer accepts
        TicketStatus.CLOSED, # Reviewer rejects
    },
    TicketStatus.WAITING: {
        TicketStatus.OPEN, # Driver updates info
        TicketStatus.CLOSED, # Reviewer/Driver cancels/closes ticket
    },
    TicketStatus.ACCEPTED: {
        TicketStatus.FIXED, # Driver gets back the car from mechanic and update the ticket
        TicketStatus.CLOSED, # Ticket canceled before work
    },
    TicketStatus.FIXED: {
        TicketStatus.WAITING_FOR_CONFIRMATION, # driver uploads receipts & photos
        TicketStatus.CONFIRMED, # no need to check anything, reviewer instant confirm
    },
    TicketStatus.WAITING_FOR_CONFIRMATION: {
        TicketStatus.CONFIRMED, # Accountant approves
        TicketStatus.PENDING, # accountant find something wrong in the confirmation
    },
    TicketStatus.PENDING: {
        TicketStatus.WAITING_FOR_CONFIRMATION,
        TicketStatus.CLOSED,
    },
    TicketStatus.CONFIRMED: {
        TicketStatus.FIXED
    },
    TicketStatus.CLOSED: set(),
}

def validate_status_transitions(current_status: TicketStatus, new_status:TicketStatus) -> None:
    if current_status == new_status:
        return
    allowed = ALLOWED_TRANSITIONS.get(current_status, set())
    if new_status not in allowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Invalid status transition")

def get_all_tickets(db: Session):
    ticket = ticket_repository.get_all_tickets(db)
    return ticket

def get_ticket(db: Session, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No ticket with ID found")
    return ticket

def create_ticket(db: Session, newTicket: TicketCreate, current_user: User):
    calculated_price = sum(item.price for item in newTicket.items)
    user = driver_user_repository.get_driver_by_user_id(db, current_user.id)
    if not user or not user.driver_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Current user does not have a driver profile")   

    assigned_vehicle_id = user.driver_profile.assigned_vehicle_id
    if not assigned_vehicle_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Current driver does not have a vehicle assigned")
    
    new_ticket = Tickets(
        title = newTicket.title,
        description = newTicket.description,
        vehicle_id = assigned_vehicle_id,
        total_price = calculated_price
    )

    for item_data in newTicket.items:
        item_obj = TicketItem(
            maintenance_category_id = item_data.maintenance_category_id,
            maintenance_subcategory_id = item_data.maintenance_subcategory_id,
            price = item_data.price,
            item_description = item_data.item_description
        )
        new_ticket.items.append(item_obj)

    return ticket_repository.create_ticket(db, new_ticket)

def update_ticket(db: Session, updateTicket: TicketUpdate, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Ticket with ID not found")

    db_ticket = updateTicket.model_dump(exclude_unset=True)
    for key, value in db_ticket.items():
        setattr(ticket, key, value)

    return ticket_repository.update_ticket(db, ticket)


def update_ticket_status(db: Session, ticket_id: int, new_status: TicketStatus) -> Tickets:
    ticket = ticket_repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Ticket with ID is not found")
    previous_status = ticket.ticket_status
    validate_status_transitions(previous_status, new_status)
    ticket.ticket_status = new_status
    if previous_status == TicketStatus.CONFIRMED and new_status == TicketStatus.CONFIRMED: ## When it goes confirmed then closed
        history_entries = []
        for item in ticket.items:
            history_entry = MaintenanceHistory(
                vehicle_id = ticket.vehicle_id,
                ticket_id = ticket.id,
                title = ticket.title,
                description = item.item_description or ticket.description,
                price = item.price,
                maintenance_category_id = item.maintenance_category_id,
                maintenance_subcategory_id = item.maintenance_subcategory_id,
                created_at = date.today()
            )
            history_entries.append(history_entry)
        if history_entries:
            maintenance_history_repository.bulk_create_maintenance_entries(db, history_entries)
        maintenance_history_repository.maintenance_entry_history(db, history_entry)
    return ticket_repository.update_ticket_status(db, ticket)