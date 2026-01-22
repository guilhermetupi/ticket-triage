from abc import ABC, abstractmethod

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem


class UpdateTriageJobBatchItemGateway(ABC):
    @abstractmethod
    def execute(self, item: TriageJobBatchItem) -> TriageJobBatchItem:
        pass
