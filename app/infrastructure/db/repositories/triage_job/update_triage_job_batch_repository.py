from sqlalchemy.orm import Session

from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.gateways.triage_job.update_triage_job_batch_gateway import UpdateTriageJobBatchGateway
from app.infrastructure.db.mappers.triage_job_batch_mapper import TriageJobBatchMapper
from app.infrastructure.db.models import TriageJobBatchModel


class SqlAlchemyUpdateTriageJobBatchRepository(UpdateTriageJobBatchGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, batch: TriageJobBatch) -> TriageJobBatch:
        model = self._db.get(TriageJobBatchModel, batch.id)
        if model is None:
            raise RuntimeError(f"TriageJobBatch {batch.id} not found")
        model.status = batch.status
        model.total_items = batch.total_items
        self._db.flush()
        self._db.refresh(model)
        return TriageJobBatchMapper.to_entity(model)
