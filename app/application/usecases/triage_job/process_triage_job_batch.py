from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.process_triage_job_batch_command import ProcessTriageJobBatchCommand
from app.application.commands.triage_ticket_command import TriageTicketCommand
from app.application.usecases.triage_job.triage_ticket import TriageTicketUseCase
from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.domain.enums.triage_job_status import TriageJobStatus
from app.domain.gateways.triage_job.claim_triage_job_batch_item_gateway import (
    ClaimTriageJobBatchItemGateway,
)
from app.domain.gateways.triage_job.update_triage_job_batch_gateway import (
    UpdateTriageJobBatchGateway,
)
from app.domain.gateways.triage_job.update_triage_job_batch_item_gateway import (
    UpdateTriageJobBatchItemGateway,
)
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)

DEFAULT_MAX_WORKERS = 4


class ProcessTriageJobBatchUseCase:
    def __init__(
            self,
            uow,
            claim_triage_job_batch_item_gateway: Callable[[Session], ClaimTriageJobBatchItemGateway],
            update_triage_job_batch_item_gateway: Callable[[Session], UpdateTriageJobBatchItemGateway],
            update_triage_job_batch_gateway: Callable[[Session], UpdateTriageJobBatchGateway],
            triage_ticket_usecase: TriageTicketUseCase,
            max_workers: int = DEFAULT_MAX_WORKERS,
    ):
        self.uow = uow
        self._claim_triage_job_batch_item_gateway = claim_triage_job_batch_item_gateway
        self._update_triage_job_batch_item_gateway = update_triage_job_batch_item_gateway
        self._update_triage_job_batch_gateway = update_triage_job_batch_gateway
        self._triage_ticket_usecase = triage_ticket_usecase
        self._max_workers = max_workers

    def execute(self, command: ProcessTriageJobBatchCommand) -> None:
        batch = command.batch
        items = command.items
        if not items:
            return

        max_workers = min(self._max_workers, len(items))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._process_item, batch.id, item.id, item.triage_job_id)
                for item in items
            ]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    _logger.execute(
                        "exception",
                        "triage_batch_worker_failed",
                        batch_id=str(batch.id),
                    )

        completed_batch = batch.on_complete()
        self._update_batch_status(completed_batch)

    def _process_item(self, batch_id, item_id, triage_job_id) -> None:
        claimed = self._claim_item(item_id)
        if claimed is None:
            _logger.execute(
                "info",
                "triage_batch_item_skipped",
                batch_id=str(batch_id),
                item_id=str(item_id),
            )
            return

        status = TriageJobStatus.FAILED
        try:
            triage_job = self._triage_ticket_usecase.execute(
                TriageTicketCommand(triage_job_id=triage_job_id)
            )
            if triage_job is not None and triage_job.status == TriageJobStatus.DONE:
                status = TriageJobStatus.DONE
        except Exception:
            _logger.execute(
                "exception",
                "triage_batch_item_failed",
                batch_id=str(batch_id),
                item_id=str(item_id),
                triage_job_id=str(triage_job_id),
            )
        finally:
            if status == TriageJobStatus.DONE:
                updated_item = claimed.on_complete()
            else:
                updated_item = claimed.on_fail()
            self._update_item_status(updated_item)

    def _claim_item(self, item_id):
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            return self._claim_triage_job_batch_item_gateway(db).execute(item_id)

    def _update_item_status(self, item):
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            self._update_triage_job_batch_item_gateway(db).execute(item)

    def _update_batch_status(self, batch):
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            self._update_triage_job_batch_gateway(db).execute(batch)

    def _resolve_uow(self):
        uow = getattr(self, "uow", None)
        if uow is None:
            raise RuntimeError("UseCase sem self.uow (necessario para ProcessTriageJobBatchUseCase)")
        if not hasattr(uow, "__enter__") and callable(uow):
            return uow()
        return uow
