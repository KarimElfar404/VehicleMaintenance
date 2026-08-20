from fastapi import APIRouter, Depends
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import Tickets
from schemas.tickets import TicketCreate, TicketUpdate, TicketResponse
from services import tickets_service
from fastapi import status
from typing import List

router = APIRouter()

@router.get("/tickets", response_model=List[TicketResponse], tags = ["Tickets"])
def get_all_tickets(db: Session = Depends(get_db)):
    return tickets_service.get_all_tickets(db)

@router.get("/tickets/{ticket_id}", response_model=TicketResponse, tags = ["Tickets"])
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return tickets_service.get_ticket(db, ticket_id)

@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED, tags = ["Tickets"])
def create_ticket(newTicket: TicketCreate, db: Session = Depends(get_db)):
    return tickets_service.create_ticket(db, newTicket)

@router.patch("/tickets/{ticket_id}", response_model=TicketResponse, status_code=status.HTTP_200_OK, tags = ["Tickets"])
def update_ticket(ticket_id: int, updateTicket: TicketUpdate, db: Session = Depends(get_db)):
    return tickets_service.update_ticket(db, updateTicket, ticket_id)

@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Tickets"])
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return tickets_service.delete_ticket(db, ticket_id)