from fastapi import APIRouter, Depends
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import Tickets
from core.security import get_current_user
from database.models import User
from schemas.tickets import TicketCreate, TicketUpdate, TicketResponse, TicketStatus
from services import tickets_service
from fastapi import HTTPException, status
from fastapi import status
from typing import List
from database.models import User
from role_permissions import require_permission

router = APIRouter()

@router.get("/tickets", response_model=List[TicketResponse], tags = ["Tickets"])
def get_all_tickets(db: Session = Depends(get_db), current_user: User = Depends(require_permission("ticket:read"))):
    return tickets_service.get_all_tickets(db)

@router.get("/tickets/{ticket_id}", response_model=TicketResponse, tags = ["Tickets"])
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("ticket:read"))):
    return tickets_service.get_ticket(db, ticket_id)

@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED, tags = ["Tickets"])
def create_ticket(
    newTicket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("ticket:create")),
):
    return tickets_service.create_ticket(db, newTicket, current_user)

@router.patch("/tickets/{ticket_id}", response_model=TicketResponse, status_code=status.HTTP_200_OK, tags = ["Tickets"])
def update_ticket(ticket_id: int, updateTicket: TicketUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("ticket:update"))):
    return tickets_service.update_ticket(db, updateTicket, ticket_id)


@router.patch("/tickets/{ticket_id}/status", response_model=TicketResponse, tags = ["Ticket Status"])
def update_ticket_status(ticket_id: int, updateTicket: TicketStatus, db: Session = Depends(get_db), current_user: User = Depends(require_permission("ticketstatus:update"))):
    return tickets_service.update_ticket_status(db, ticket_id, updateTicket)