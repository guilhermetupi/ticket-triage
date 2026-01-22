from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.create_triage_job_batch_command import CreateTriageJobBatchCommand
from app.application.transactional import transactional
from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.domain.gateways.triage_job.create_triage_job_batch_gateway import (
    CreateTriageJobBatchGateway,
)
from app.domain.gateways.triage_job.create_triage_job_batch_items_gateway import (
    CreateTriageJobBatchItemsGateway,
)
from app.domain.gateways.triage_job.list_pending_triage_jobs_gateway import (
    ListPendingTriageJobsGateway,
)
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)


class CreateTriageJobBatchUseCase:
    def __init__(
            self,
            uow,
            list_pending_triage_jobs_gateway: Callable[[Session], ListPendingTriageJobsGateway],
            create_triage_job_batch_gateway: Callable[[Session], CreateTriageJobBatchGateway],
            create_triage_job_batch_items_gateway: Callable[[Session], CreateTriageJobBatchItemsGateway],
    ):
        self.uow = uow
        self._list_pending_triage_jobs_gateway = list_pending_triage_jobs_gateway
        self._create_triage_job_batch_gateway = create_triage_job_batch_gateway
        self._create_triage_job_batch_items_gateway = create_triage_job_batch_items_gateway

    @transactional
    def execute(
            self,
            command: CreateTriageJobBatchCommand,
            *,
            db: Session | None = None,
    ) -> tuple[TriageJobBatch | None, list[TriageJobBatchItem]]:
        assert db is not None
        jobs = self._list_pending_triage_jobs_gateway(db).execute()
        if not jobs:
            _logger.execute("info", "triage_batch_empty")
            return None, []

        _logger.execute("info", "triage_batch_create_started", total_items=len(jobs))
        batch = TriageJobBatch.create(total_items=len(jobs))
        batch = self._create_triage_job_batch_gateway(db).execute(batch)

        items = [TriageJobBatchItem.create(batch.id, job.id) for job in jobs]
        self._create_triage_job_batch_items_gateway(db).execute(items)
        _logger.execute(
            "info",
            "triage_batch_created",
            batch_id=str(batch.id),
            total_items=len(items),
        )
        return batch, items
