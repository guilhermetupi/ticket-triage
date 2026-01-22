import uuid
from sqlalchemy.orm import Session
from app.domain.entities.triage_job import TriageJob
from app.domain.gateways.triage_job.find_triage_job_by_id_gateway import FindTriageJobByTicketIdGateway
from app.infrastructure.db.mappers.triage_job_mapper import TriageJobMapper
from app.infrastructure.db.models import TriageJobModel


class SqlAlchemyFindTriageJobByTicketIdRepository(FindTriageJobByTicketIdGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, ticket_id: uuid.UUID) -> TriageJob | None:
        model: TriageJobModel | None = (self._db.query(TriageJobModel)
                                        .filter(TriageJobModel.ticket_id == ticket_id).one_or_none())

        if model is None:
            return None

        return TriageJobMapper.to_entity(model)
