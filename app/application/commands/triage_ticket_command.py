import uuid

from pydantic import BaseModel


class TriageTicketCommand(BaseModel):
    triage_job_id: uuid.UUID | None = None
