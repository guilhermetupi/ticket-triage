from sqlalchemy.orm import Session
from app.domain.entities.triage_job import TriageJob
from app.domain.gateways.triage_job.create_triage_job_gateway import CreateTriageJobGateway
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper


class SqlAlchemyCreateTriageJobRepository(CreateTriageJobGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, triage_job: TriageJob) -> TriageJob:
        model = TriageJobMapper.to_model(triage_job)
        self._db.add(model)
        self._db.flush()
        self._db.refresh(model)
        return TriageJobMapper.to_entity(model)
