from abc import ABC, abstractmethod

from app.domain.entities.triage_job_batch import TriageJobBatch


class UpdateTriageJobBatchGateway(ABC):
    @abstractmethod
    def execute(self, batch: TriageJobBatch) -> TriageJobBatch:
        pass
