import uuid

from sqlalchemy.orm import Session

from app.domain.entities.ticket import Ticket
from app.domain.gateways.ticket.find_ticket_by_id_gateway import FindTicketByIdGateway
from app.infrastructure.db.mappers.ticket_mapper import TicketMapper
from app.infrastructure.db.models import TicketModel


class SqlAlchemyFindTicketByIdRepository(FindTicketByIdGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, ticket_id: uuid.UUID) -> Ticket | None:
        model = self._db.get(TicketModel, ticket_id)
        if model is None:
            return None
        return TicketMapper.to_entity(model)
