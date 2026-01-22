import uuid
from datetime import datetime
from dataclasses import dataclass

from app.domain.entities.base_entity import BaseEntity
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.exceptions.triage_job_exception_code import TRIAGE_JOB_EXCEPTION
from app.domain.exceptions.unprocessable_entity_exception import UnprocessableEntityException


@dataclass(frozen=True)
class TriageJobBatchItem(BaseEntity):
    batch_id: uuid.UUID
    triage_job_id: uuid.UUID
    status: TriageJobStatus = TriageJobStatus.PENDING

    @staticmethod
    def create(
            batch_id: uuid.UUID,
            triage_job_id: uuid.UUID,
            status: TriageJobStatus = TriageJobStatus.PENDING,
    ):
        return TriageJobBatchItem(
            id=uuid.uuid4(),
            batch_id=batch_id,
            triage_job_id=triage_job_id,
            status=status,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            batch_id: uuid.UUID,
            triage_job_id: uuid.UUID,
            status: TriageJobStatus,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime,
    ):
        return TriageJobBatchItem(
            id=id,
            batch_id=batch_id,
            triage_job_id=triage_job_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

    def on_running(self):
        if self.status != TriageJobStatus.PENDING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.RUNNING},
            )
        return TriageJobBatchItem.reconstitute(**{**self.__dict__, "status": TriageJobStatus.RUNNING})

    def on_complete(self):
        if self.status != TriageJobStatus.RUNNING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.DONE},
            )
        return TriageJobBatchItem.reconstitute(**{**self.__dict__, "status": TriageJobStatus.DONE})

    def on_fail(self):
        if self.status != TriageJobStatus.RUNNING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.FAILED},
            )
        return TriageJobBatchItem.reconstitute(**{**self.__dict__, "status": TriageJobStatus.FAILED})
