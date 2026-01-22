from sqlalchemy.orm import Session
from app.domain.entities.ticket import Ticket
from app.domain.gateways.ticket.find_ticket_by_external_id import FindTicketByExternalIdGateway
from app.infrastructure.db.mappers.ticket_mapper import TicketMapper
from app.infrastructure.db.models.ticket import TicketModel


class SqlAlchemyFindTicketByExternalIdRepository(FindTicketByExternalIdGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, external_id: str) -> Ticket | None:
        model: TicketModel | None = (self._db.query(TicketModel)
                                     .filter(TicketModel.external_id == external_id).one_or_none())

        if model is None:
            return None

        return TicketMapper.to_entity(model)
