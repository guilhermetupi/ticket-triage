from sqlalchemy.orm import Session
from app.domain.entities.ticket import Ticket
from app.domain.gateways.ticket.create_ticket_gateway import CreateTicketGateway
from app.infrastructure.db.mappers.ticket_mapper import TicketMapper


class SqlAlchemyCreateTicketRepository(CreateTicketGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, ticket: Ticket) -> Ticket:
        model = TicketMapper.to_model(ticket)
        self._db.add(model)
        self._db.flush()
        self._db.refresh(model)
        return TicketMapper.to_entity(model)
