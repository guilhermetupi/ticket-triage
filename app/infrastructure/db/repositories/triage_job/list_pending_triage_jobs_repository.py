from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.triage_job import TriageJob
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.gateways.triage_job.list_pending_triage_jobs_gateway import ListPendingTriageJobsGateway
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper
from app.infrastructure.db.models import TriageJobModel


class SqlAlchemyListPendingTriageJobsRepository(ListPendingTriageJobsGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self) -> list[TriageJob]:
        stmt = (
            select(TriageJobModel)
            .where(
                TriageJobModel.status.in_((TriageJobStatus.PENDING, TriageJobStatus.FAILED)),
                TriageJobModel.attempts < 3,
                TriageJobModel.deleted_at.is_(None),
            )
            .order_by(TriageJobModel.created_at.asc())
        )
        rows = self._db.execute(stmt).scalars().all()
        return [TriageJobMapper.to_entity(model) for model in rows]
