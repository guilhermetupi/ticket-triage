from sqlalchemy.orm import Session

from app.domain.entities.triage_job_log import TriageJobLog
from app.domain.gateways.triage_job.create_triage_job_log_gateway import CreateTriageJobLogGateway
from app.infrastructure.db.mappers.triage_job_log_mapper import TriageJobLogMapper


class SqlAlchemyCreateTriageJobLogRepository(CreateTriageJobLogGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, triage_job_log: TriageJobLog) -> TriageJobLog:
        model = TriageJobLogMapper.to_model(triage_job_log)
        self._db.add(model)
        self._db.flush()
        self._db.refresh(model)
        return TriageJobLogMapper.to_entity(model)
