import uuid
from datetime import datetime
from dataclasses import dataclass
from app.domain.entities.base_entity import BaseEntity


@dataclass(frozen=True)
class TriageJobLog(BaseEntity):
    success: bool
    input: str
    output: str
    prompt_id: uuid.UUID | None
    triage_job_id: uuid.UUID

    @staticmethod
    def create(
            input: str,
            output: str,
            prompt_id: uuid.UUID | None,
            success: bool,
            triage_job_id: uuid.UUID,
    ):
        return TriageJobLog(
            id=uuid.uuid4(),
            success=success,
            input=input,
            output=output,
            prompt_id=prompt_id,
            triage_job_id=triage_job_id,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            input: str,
            output: str,
            prompt_id: uuid.UUID | None,
            success: bool,
            triage_job_id: uuid.UUID,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime
    ):
        return TriageJobLog(
            id=id,
            success=success,
            input=input,
            output=output,
            prompt_id=prompt_id,
            triage_job_id=triage_job_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )
