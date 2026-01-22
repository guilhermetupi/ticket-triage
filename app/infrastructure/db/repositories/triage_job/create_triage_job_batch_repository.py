from sqlalchemy.orm import Session

from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.gateways.triage_job.create_triage_job_batch_gateway import CreateTriageJobBatchGateway
from app.infrastructure.db.mappers.triage_job_batch_mapper import TriageJobBatchMapper


class SqlAlchemyCreateTriageJobBatchRepository(CreateTriageJobBatchGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, batch: TriageJobBatch) -> TriageJobBatch:
        model = TriageJobBatchMapper.to_model(batch)
        self._db.add(model)
        self._db.flush()
        self._db.refresh(model)
        return TriageJobBatchMapper.to_entity(model)
