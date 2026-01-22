from abc import ABC, abstractmethod

from app.domain.entities.triage_job import TriageJob


class ListPendingTriageJobsGateway(ABC):
    @abstractmethod
    def execute(self) -> list[TriageJob]:
        pass
