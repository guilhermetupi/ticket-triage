import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import List
from app.domain.entities.base_entity import BaseEntity
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.exceptions.triage_job_exception_code import TRIAGE_JOB_EXCEPTION
from app.domain.exceptions.unprocessable_entity_exception import UnprocessableEntityException


@dataclass(frozen=True)
class TriageJob(BaseEntity):
    ticket_id: uuid.UUID
    status: TriageJobStatus = TriageJobStatus.PENDING
    attempts: int = 0
    log_ids: List[uuid.UUID] | None = None

    @staticmethod
    def create(
            ticket_id: uuid.UUID,
            status: TriageJobStatus = TriageJobStatus.PENDING,
            log_ids: List[uuid.UUID] | None = None,
            attempts: int | None = 0
    ):
        return TriageJob(
            id=uuid.uuid4(),
            status=status,
            attempts=TriageJob.parse_attempts(attempts=attempts, log_ids=log_ids),
            ticket_id=ticket_id,
            log_ids=log_ids,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            ticket_id: uuid.UUID,
            status: TriageJobStatus,
            attempts: int | None,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime,
            log_ids: List[uuid.UUID] | None = None,
    ):
        return TriageJob(
            id=id,
            status=status,
            attempts=TriageJob.parse_attempts(attempts=attempts, log_ids=log_ids),
            log_ids=log_ids,
            ticket_id=ticket_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

    @staticmethod
    def parse_attempts(attempts: int = 0, log_ids: List[uuid.UUID] = None) -> int:
        final_attempts = attempts
        if log_ids is not None and len(log_ids) > 0:
            final_attempts = len(log_ids)
        if final_attempts < 0:
            raise UnprocessableEntityException(**TRIAGE_JOB_EXCEPTION['NEGATIVE_ATTEMPTS'])
        return final_attempts

    def on_running(self):
        if self.status not in (TriageJobStatus.PENDING, TriageJobStatus.FAILED):
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.RUNNING}
            )
        data = {**self.__dict__, "status": TriageJobStatus.RUNNING, "attempts": self.attempts + 1}
        return TriageJob.reconstitute(**data)

    def on_complete(self):
        if self.status != TriageJobStatus.RUNNING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.DONE}
            )
        data = {**self.__dict__, "status": TriageJobStatus.DONE}
        return TriageJob.reconstitute(**data)

    def on_fail(self):
        if self.status != TriageJobStatus.RUNNING:
            raise UnprocessableEntityException(
                **TRIAGE_JOB_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": self.status, "new_status": TriageJobStatus.FAILED}
            )
        data = {**self.__dict__, "status": TriageJobStatus.FAILED}
        return TriageJob.reconstitute(**data)
