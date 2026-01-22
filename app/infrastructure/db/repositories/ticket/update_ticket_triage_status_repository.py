from sqlalchemy.orm import Session

from app.domain.entities.ticket import Ticket
from app.domain.gateways.ticket.update_ticket_triage_status_gateway import UpdateTicketTriageStatusGateway
from app.infrastructure.db.mappers.ticket_mapper import TicketMapper
from app.infrastructure.db.models import TicketModel


class SqlAlchemyUpdateTicketTriageStatusRepository(UpdateTicketTriageStatusGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, ticket: Ticket) -> Ticket | None:
        model = self._db.get(TicketModel, ticket.id)
        if model is None:
            return
        model.triage_status = ticket.triage_status
        self._db.flush()
        self._db.refresh(model)
        return TicketMapper.to_entity(model)
