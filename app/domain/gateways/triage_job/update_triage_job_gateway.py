from abc import ABC, abstractmethod

from app.domain.entities.triage_job import TriageJob


class UpdateTriageJobGateway(ABC):
    @abstractmethod
    def execute(self, triage_job: TriageJob) -> TriageJob:
        pass
