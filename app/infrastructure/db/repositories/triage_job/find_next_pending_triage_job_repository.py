from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.entities.triage_job import TriageJob
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.gateways.triage_job.find_next_pending_triage_job_gateway import FindNextPendingTriageJobDatabaseGateway
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper
from app.infrastructure.db.models import TriageJobModel


class SqlAlchemyFindNextPendingTriageJobRepository(FindNextPendingTriageJobDatabaseGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self) -> TriageJob | None:
        stmt = (
            select(TriageJobModel)
            .where(
                TriageJobModel.status.in_((TriageJobStatus.PENDING, TriageJobStatus.FAILED)),
                TriageJobModel.attempts < 3,
                TriageJobModel.deleted_at.is_(None),
            )
            .order_by(TriageJobModel.created_at.asc())
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        model = self._db.execute(stmt).scalar_one_or_none()

        if model is None:
            return None

        return TriageJobMapper.to_entity(model)
