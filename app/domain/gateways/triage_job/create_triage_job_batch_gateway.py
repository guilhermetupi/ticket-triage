from abc import ABC, abstractmethod

from app.domain.entities.triage_job_batch import TriageJobBatch


class CreateTriageJobBatchGateway(ABC):
    @abstractmethod
    def execute(self, batch: TriageJobBatch) -> TriageJobBatch:
        pass
