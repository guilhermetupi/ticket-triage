from app.domain.entities.ticket import Ticket
from app.infrastructure.db.models import TicketModel


class TicketMapper:
    @staticmethod
    def to_model(entity: Ticket) -> TicketModel:
        return TicketModel(**entity.__dict__)

    @staticmethod
    def to_entity(model: TicketModel) -> Ticket:
        return Ticket.reconstitute(
            id=model.id,
            title=model.title,
            description=model.description,
            triage_status=model.triage_status,
            external_id=model.external_id,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
