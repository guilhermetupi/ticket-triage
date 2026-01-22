from datetime import datetime
import uuid
from pydantic import BaseModel
from app.domain.enums.ticket_triage_status import TicketTriageStatus


class TicketResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    external_id: str
    owner_id: uuid.UUID
    triage_status: TicketTriageStatus
    created_at: datetime
    updated_at: datetime