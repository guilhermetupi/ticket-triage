import uuid
from abc import ABC, abstractmethod

from app.domain.entities.triage_job import TriageJob


class FindTriageJobByTicketIdGateway(ABC):
    @abstractmethod
    def execute(self, ticket_id: uuid.UUID) -> TriageJob | None:
        pass
