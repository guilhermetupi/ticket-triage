import uuid
from pydantic import BaseModel


class CreateTriageJobCommand(BaseModel):
    ticket_id: uuid.UUID
