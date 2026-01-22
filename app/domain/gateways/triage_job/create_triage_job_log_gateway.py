from abc import ABC, abstractmethod

from app.domain.entities.triage_job_log import TriageJobLog


class CreateTriageJobLogGateway(ABC):
    @abstractmethod
    def execute(self, triage_job_log: TriageJobLog) -> TriageJobLog:
        pass
