from abc import ABC, abstractmethod
from app.domain.entities.triage_job import TriageJob


class FindNextPendingTriageJobDatabaseGateway(ABC):
    @abstractmethod
    def execute(self) -> TriageJob | None:
        pass
