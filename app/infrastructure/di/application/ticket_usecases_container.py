from dependency_injector import providers, containers

from app.application.usecases.ticket.create_ticket_usecase import CreateTicketUseCase
from app.infrastructure.di.application.triage_job_usecases_container import TriageJobUseCasesContainer
from app.infrastructure.di.infrastructure.db.ticket_repositories_container import TicketDatabaseRepositoriesContainer
from app.infrastructure.db.session import create_db_session
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


class TicketUseCasesContainer(containers.DeclarativeContainer):
    ticket_database_repositories_container = providers.Container(TicketDatabaseRepositoriesContainer)
    triage_job_usecases_container = providers.Container(TriageJobUseCasesContainer)
    uow = providers.Factory(SqlAlchemyUnitOfWork, session_factory=create_db_session)
    create_ticket_usecase = providers.Factory(
        CreateTicketUseCase,
        uow=uow.provider,
        create_ticket_database_gateway=ticket_database_repositories_container.create_ticket.provider,
        find_ticket_by_external_id=ticket_database_repositories_container.find_ticket_by_external_id.provider,
        create_triage_job_usecase=triage_job_usecases_container.create_triage_job_usecase,
    )
