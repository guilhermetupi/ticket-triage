from sqlalchemy.orm import Session

from app.domain.entities.triage_job import TriageJob
from app.domain.gateways.triage_job.update_triage_job_gateway import UpdateTriageJobGateway
from app.infrastructure.db.models import TriageJobModel
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper


class SqlAlchemyUpdateTriageJobRepository(UpdateTriageJobGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, triage_job: TriageJob) -> TriageJob:
        model = self._db.get(TriageJobModel, triage_job.id)
        if model is None:
            model = TriageJobMapper.to_model(triage_job)
            self._db.add(model)
        else:
            model.status = triage_job.status
            model.attempts = triage_job.attempts
        self._db.flush()
        self._db.refresh(model)
        return TriageJobMapper.to_entity(model)
