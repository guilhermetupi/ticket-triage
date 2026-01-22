import uuid
from abc import ABC, abstractmethod

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem


class ClaimTriageJobBatchItemGateway(ABC):
    @abstractmethod
    def execute(self, item_id: uuid.UUID) -> TriageJobBatchItem | None:
        pass
