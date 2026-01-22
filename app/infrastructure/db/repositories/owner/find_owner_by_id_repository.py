import uuid
from sqlalchemy.orm import Session
from app.domain.entities.owner import Owner
from app.domain.gateways.triage_job.find_owner_by_ticket_id_gateway import FindOwnerByIdGateway
from app.infrastructure.db.mappers.owner_mapper import OwnerMapper
from app.infrastructure.db.models import OwnerModel


class SqlAlchemyFindOwnerByIdRepository(FindOwnerByIdGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, id: uuid.UUID) -> Owner | None:
        model: OwnerModel | None = self._db.get(OwnerModel, id)

        if model is None:
            return None

        return OwnerMapper.to_entity(model)
