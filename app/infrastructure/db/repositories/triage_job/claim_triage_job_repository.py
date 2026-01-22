import uuid

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.domain.entities.triage_job import TriageJob
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.gateways.triage_job.claim_triage_job_gateway import ClaimTriageJobGateway
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper
from app.infrastructure.db.models import TriageJobModel


class SqlAlchemyClaimTriageJobRepository(ClaimTriageJobGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, triage_job_id: uuid.UUID) -> TriageJob | None:
        stmt = (
            update(TriageJobModel)
            .where(
                TriageJobModel.id == triage_job_id,
                TriageJobModel.status.in_((TriageJobStatus.PENDING, TriageJobStatus.FAILED)),
                TriageJobModel.attempts < 3,
                TriageJobModel.deleted_at.is_(None),
            )
            .values(
                status=TriageJobStatus.RUNNING,
                attempts=TriageJobModel.attempts + 1,
            )
            .returning(TriageJobModel.id)
        )
        row = self._db.execute(stmt).scalar_one_or_none()
        if row is None:
            return None
        model = self._db.get(TriageJobModel, row)
        if model is None:
            return None
        return TriageJobMapper.to_entity(model)
