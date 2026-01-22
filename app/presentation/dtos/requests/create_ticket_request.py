import uuid

from pydantic import BaseModel, UUID4


class CreateTicketRequest(BaseModel):
    title: str
    description: str
    external_id: str
    owner_id: uuid.UUID
