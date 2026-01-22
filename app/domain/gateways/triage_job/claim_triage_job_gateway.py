import uuid
from abc import ABC, abstractmethod

from app.domain.entities.triage_job import TriageJob


class ClaimTriageJobGateway(ABC):
    @abstractmethod
    def execute(self, triage_job_id: uuid.UUID) -> TriageJob | None:
        pass
