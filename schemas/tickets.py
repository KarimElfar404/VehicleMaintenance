from pydantic import BaseModel
from enum import Enum
from typing import List
class TicketStatus(str, Enum):
    OPEN = "Open"
    WAITING = "Waiting Reply"
    WAITING_FOR_CONFIRMATION = "Waiting for confirmation"
    ACCEPTED = "Accepted"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    FIXED = "Fixed"
    CLOSED = "Closed"

class TicketItemCreate(BaseModel):
    maintenance_category_id: int
    maintenance_subcategory_id: int
    price: float
    item_description: str | None = None
class TicketCreate(BaseModel):
    title: str
    description: str
    items: List[TicketItemCreate]

class TicketItemResponse(BaseModel):
    id: int
    maintenance_category_id: int
    maintenance_subcategory_id: int
    price: float
    item_description: str | None = None
    class Config:
        from_attributes = True

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
    total_price: int
    vehicle_id: int
    items: List[TicketItemResponse]

    class Config:
        from_attributes = True
