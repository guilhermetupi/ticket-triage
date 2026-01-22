from dependency_injector import providers, containers

from app.application.usecases.triage_job.find_next_pending_triage_job import FindNextPendingTriageJobUseCase
from app.application.usecases.triage_job.create_triage_job import CreateTriageJobUseCase
from app.application.usecases.triage_job.create_triage_job_batch import CreateTriageJobBatchUseCase
from app.application.usecases.triage_job.process_triage_job_batch import ProcessTriageJobBatchUseCase
from app.application.usecases.triage_job.triage_ticket import TriageTicketUseCase
from app.infrastructure.di.infrastructure.db.prompt_repositories_container import PromptDatabaseRepositoriesContainer
from app.infrastructure.di.infrastructure.db.ticket_repositories_container import TicketDatabaseRepositoriesContainer
from app.infrastructure.di.infrastructure.db.triage_job_repositories_container import \
    TriageJobDatabaseRepositoriesContainer
from app.infrastructure.di.infrastructure.llm.llm_client_container import (
    TicketDatabaseRepositoriesContainer as LLMClientContainer,
)
from app.infrastructure.db.session import create_db_session
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


class TriageJobUseCasesContainer(containers.DeclarativeContainer):
    triage_job_database_repositories_container = providers.Container(TriageJobDatabaseRepositoriesContainer)
    ticket_database_repositories_container = providers.Container(TicketDatabaseRepositoriesContainer)
    prompt_database_repositories_container = providers.Container(PromptDatabaseRepositoriesContainer)
    llm_client_container = providers.Container(LLMClientContainer)
    uow = providers.Factory(SqlAlchemyUnitOfWork, session_factory=create_db_session)
    create_triage_job_usecase = providers.Factory(
        CreateTriageJobUseCase,
        uow=uow.provider,
        create_triage_job_gateway=triage_job_database_repositories_container.create_triage_job.provider,
        find_triage_job_by_ticket_id_gateway=triage_job_database_repositories_container.find_triage_job_by_ticket_id.provider,
    )
    find_next_pending_triage_job_usecase = providers.Factory(
        FindNextPendingTriageJobUseCase,
        uow=uow.provider,
        find_next_pending_triage_job_gateway=triage_job_database_repositories_container.find_next_pending_triage_job.provider,
    )
    triage_ticket_usecase = providers.Factory(
        TriageTicketUseCase,
        uow=uow.provider,
        client=llm_client_container.llm_client,
        find_next_pending_triage_job_gateway=triage_job_database_repositories_container.find_next_pending_triage_job.provider,
        claim_triage_job_gateway=triage_job_database_repositories_container.claim_triage_job.provider,
        update_triage_job_gateway=triage_job_database_repositories_container.update_triage_job.provider,
        find_ticket_by_id_gateway=ticket_database_repositories_container.find_ticket_by_id.provider,
        update_ticket_triage_status_gateway=ticket_database_repositories_container.update_ticket_triage_status.provider,
        find_active_prompt_gateway=prompt_database_repositories_container.find_active_prompt.provider,
        create_triage_job_log_gateway=triage_job_database_repositories_container.create_triage_job_log.provider,
    )
    create_triage_job_batch_usecase = providers.Factory(
        CreateTriageJobBatchUseCase,
        uow=uow.provider,
        list_pending_triage_jobs_gateway=triage_job_database_repositories_container.list_pending_triage_jobs.provider,
        create_triage_job_batch_gateway=triage_job_database_repositories_container.create_triage_job_batch.provider,
        create_triage_job_batch_items_gateway=triage_job_database_repositories_container.create_triage_job_batch_items.provider,
    )
    process_triage_job_batch_usecase = providers.Factory(
        ProcessTriageJobBatchUseCase,
        uow=uow.provider,
        claim_triage_job_batch_item_gateway=triage_job_database_repositories_container.claim_triage_job_batch_item.provider,
        update_triage_job_batch_item_gateway=triage_job_database_repositories_container.update_triage_job_batch_item.provider,
        update_triage_job_batch_gateway=triage_job_database_repositories_container.update_triage_job_batch.provider,
        triage_ticket_usecase=triage_ticket_usecase,
    )
