from app.infrastructure.db.repositories.triage_job.create_triage_job_log_repository import (
    SqlAlchemyCreateTriageJobLogRepository,
)
from app.infrastructure.db.repositories.triage_job.create_triage_job_repository import SqlAlchemyCreateTriageJobRepository
from app.infrastructure.db.repositories.triage_job.create_triage_job_batch_items_repository import (
    SqlAlchemyCreateTriageJobBatchItemsRepository,
)
from app.infrastructure.db.repositories.triage_job.create_triage_job_batch_repository import (
    SqlAlchemyCreateTriageJobBatchRepository,
)
from app.infrastructure.db.repositories.triage_job.claim_triage_job_batch_item_repository import (
    SqlAlchemyClaimTriageJobBatchItemRepository,
)
from app.infrastructure.db.repositories.triage_job.claim_triage_job_repository import (
    SqlAlchemyClaimTriageJobRepository,
)
from app.infrastructure.db.repositories.triage_job.find_next_pending_triage_job_repository import (
    SqlAlchemyFindNextPendingTriageJobRepository,
)
from app.infrastructure.db.repositories.triage_job.find_triage_job_by_ticket_id_repository import (
    SqlAlchemyFindTriageJobByTicketIdRepository,
)
from app.infrastructure.db.repositories.triage_job.list_pending_triage_jobs_repository import (
    SqlAlchemyListPendingTriageJobsRepository,
)
from app.infrastructure.db.repositories.triage_job.update_triage_job_repository import (
    SqlAlchemyUpdateTriageJobRepository,
)
from app.infrastructure.db.repositories.triage_job.update_triage_job_batch_item_repository import (
    SqlAlchemyUpdateTriageJobBatchItemRepository,
)
from app.infrastructure.db.repositories.triage_job.update_triage_job_batch_repository import (
    SqlAlchemyUpdateTriageJobBatchRepository,
)
from dependency_injector import containers, providers


class TriageJobDatabaseRepositoriesContainer(containers.DeclarativeContainer):
    create_triage_job = providers.Factory(SqlAlchemyCreateTriageJobRepository)
    find_triage_job_by_ticket_id = providers.Factory(SqlAlchemyFindTriageJobByTicketIdRepository)
    find_next_pending_triage_job = providers.Factory(SqlAlchemyFindNextPendingTriageJobRepository)
    update_triage_job = providers.Factory(SqlAlchemyUpdateTriageJobRepository)
    create_triage_job_log = providers.Factory(SqlAlchemyCreateTriageJobLogRepository)
    list_pending_triage_jobs = providers.Factory(SqlAlchemyListPendingTriageJobsRepository)
    create_triage_job_batch = providers.Factory(SqlAlchemyCreateTriageJobBatchRepository)
    create_triage_job_batch_items = providers.Factory(SqlAlchemyCreateTriageJobBatchItemsRepository)
    claim_triage_job_batch_item = providers.Factory(SqlAlchemyClaimTriageJobBatchItemRepository)
    update_triage_job_batch_item = providers.Factory(SqlAlchemyUpdateTriageJobBatchItemRepository)
    update_triage_job_batch = providers.Factory(SqlAlchemyUpdateTriageJobBatchRepository)
    claim_triage_job = providers.Factory(SqlAlchemyClaimTriageJobRepository)
