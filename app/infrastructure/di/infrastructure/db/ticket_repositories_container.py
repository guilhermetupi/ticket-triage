from app.infrastructure.db.repositories.ticket.create_ticket_repository import SqlAlchemyCreateTicketRepository
from app.infrastructure.db.repositories.ticket.find_ticket_by_external_id_repository import (
    SqlAlchemyFindTicketByExternalIdRepository,
)
from app.infrastructure.db.repositories.ticket.find_ticket_by_id_repository import (
    SqlAlchemyFindTicketByIdRepository,
)
from app.infrastructure.db.repositories.ticket.update_ticket_triage_status_repository import (
    SqlAlchemyUpdateTicketTriageStatusRepository,
)
from dependency_injector import containers, providers


class TicketDatabaseRepositoriesContainer(containers.DeclarativeContainer):
    create_ticket = providers.Factory(SqlAlchemyCreateTicketRepository)
    find_ticket_by_external_id = providers.Factory(SqlAlchemyFindTicketByExternalIdRepository)
    find_ticket_by_id = providers.Factory(SqlAlchemyFindTicketByIdRepository)
    update_ticket_triage_status = providers.Factory(SqlAlchemyUpdateTicketTriageStatusRepository)
