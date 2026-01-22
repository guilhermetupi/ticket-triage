import uuid

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.gateways.triage_job.claim_triage_job_batch_item_gateway import ClaimTriageJobBatchItemGateway
from app.infrastructure.db.mappers.triage_job_batch_item_mapper import TriageJobBatchItemMapper
from app.infrastructure.db.models import TriageJobBatchItemModel


class SqlAlchemyClaimTriageJobBatchItemRepository(ClaimTriageJobBatchItemGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, item_id: uuid.UUID) -> TriageJobBatchItem | None:
        stmt = (
            update(TriageJobBatchItemModel)
            .where(
                TriageJobBatchItemModel.id == item_id,
                TriageJobBatchItemModel.status == TriageJobStatus.PENDING,
                TriageJobBatchItemModel.deleted_at.is_(None),
            )
            .values(status=TriageJobStatus.RUNNING)
            .returning(TriageJobBatchItemModel.id)
        )
        row = self._db.execute(stmt).scalar_one_or_none()
        if row is None:
            return None
        model = self._db.get(TriageJobBatchItemModel, row)
        if model is None:
            return None
        return TriageJobBatchItemMapper.to_entity(model)
