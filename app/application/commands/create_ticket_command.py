import uuid
from pydantic import BaseModel


class CreateTicketCommand(BaseModel):
    title: str
    description: str
    external_id: str
    owner_id: uuid.UUID
