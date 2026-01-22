from abc import ABC, abstractmethod

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem


class CreateTriageJobBatchItemsGateway(ABC):
    @abstractmethod
    def execute(self, items: list[TriageJobBatchItem]) -> list[TriageJobBatchItem]:
        pass
