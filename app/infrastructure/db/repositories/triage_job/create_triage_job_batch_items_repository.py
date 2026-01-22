from sqlalchemy.orm import Session

from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.domain.gateways.triage_job.create_triage_job_batch_items_gateway import CreateTriageJobBatchItemsGateway
from app.infrastructure.db.mappers.triage_job_batch_item_mapper import TriageJobBatchItemMapper


class SqlAlchemyCreateTriageJobBatchItemsRepository(CreateTriageJobBatchItemsGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, items: list[TriageJobBatchItem]) -> list[TriageJobBatchItem]:
        models = [TriageJobBatchItemMapper.to_model(item) for item in items]
        self._db.add_all(models)
        self._db.flush()
        return items
