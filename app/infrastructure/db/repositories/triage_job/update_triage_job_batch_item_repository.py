from sqlalchemy import update
from sqlalchemy.orm import Session

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.domain.gateways.triage_job.update_triage_job_batch_item_gateway import UpdateTriageJobBatchItemGateway
from app.infrastructure.db.mappers.triage_job_batch_item_mapper import TriageJobBatchItemMapper
from app.infrastructure.db.models import TriageJobBatchItemModel


class SqlAlchemyUpdateTriageJobBatchItemRepository(UpdateTriageJobBatchItemGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, item: TriageJobBatchItem) -> TriageJobBatchItem:
        stmt = (
            update(TriageJobBatchItemModel)
            .where(TriageJobBatchItemModel.id == item.id)
            .values(status=item.status)
            .returning(TriageJobBatchItemModel.id)
        )
        row = self._db.execute(stmt).scalar_one_or_none()
        if row is None:
            raise RuntimeError(f"TriageJobBatchItem {item.id} not found")
        model = self._db.get(TriageJobBatchItemModel, row)
        if model is None:
            raise RuntimeError(f"TriageJobBatchItem {item.id} not found")
        return TriageJobBatchItemMapper.to_entity(model)
