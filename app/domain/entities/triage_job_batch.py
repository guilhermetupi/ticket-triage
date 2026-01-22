import uuid
from datetime import datetime
from dataclasses import dataclass

from app.domain.entities.base_entity import BaseEntity
from app.domain.enums.triage_job_batch_status import TriageJobBatchStatus
from app.domain.exceptions.triage_job_exception_code import TRIAGE_JOB_EXCEPTION
from app.domain.exceptions.unprocessable_entity_exception import UnprocessableEntityException


@dataclass(frozen=True)
class TriageJobBatch(BaseEntity):
    status: TriageJobBatchStatus
    total_items: int

    @staticmethod
    def create(
            total_items: int,
            status: TriageJobBatchStatus = TriageJobBatchStatus.RUNNING,
    ):
        return TriageJobBatch(
            id=uuid.uuid4(),
            status=status,
            total_items=total_items,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            status: TriageJobBatchStatus,
            total_items: int,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime,
    ):
        return TriageJobBatch(
            id=id,
            status=status,
            total_items=total_items,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

    def on_complete(self):
        if self.status != TriageJobBatchStatus.RUNNING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobBatchStatus.DONE},
            )
        return TriageJobBatch.reconstitute(**{**self.__dict__, "status": TriageJobBatchStatus.DONE})
