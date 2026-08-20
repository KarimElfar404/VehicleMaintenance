from pydantic import BaseModel
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "Open"
    WAITING = "Waiting Reply"
    CLOSED = "Closed"
    ACCEPTED = "Accepted"
    PENDING = "Pending"

class TicketCreate(BaseModel):
    title: str
    ticket_status: TicketStatus = TicketStatus.OPEN
    description: str
    price: int
    maintenance_category_id: int
    maintenance_subcategory_id: int

class TicketUpdate(BaseModel):
    title: str | None = None
    ticket_status: TicketStatus | None = None
    description: str | None = None
    price: int | None = None
    maintenance_category_id: int | None = None
    maintenance_subcategory_id: int | None = None

class TicketResponse(BaseModel):
    id: int
    title: str
    ticket_status: TicketStatus = TicketStatus.OPEN
    description: str
    price: int
    maintenance_category_id: int
    maintenance_subcategory_id: int

    class Config:
        from_attributes = True
