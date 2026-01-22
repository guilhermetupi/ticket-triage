from app.application.commands.create_triage_job_batch_command import CreateTriageJobBatchCommand
from app.application.commands.process_triage_job_batch_command import ProcessTriageJobBatchCommand
from app.application.usecases.triage_job.create_triage_job_batch import CreateTriageJobBatchUseCase
from app.application.usecases.triage_job.process_triage_job_batch import ProcessTriageJobBatchUseCase
from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)


class TriageJobController:
    def __init__(
            self,
            create_triage_job_batch_usecase: CreateTriageJobBatchUseCase,
            process_triage_job_batch_usecase: ProcessTriageJobBatchUseCase,
    ):
        self._create_triage_job_batch_usecase = create_triage_job_batch_usecase
        self._process_triage_job_batch_usecase = process_triage_job_batch_usecase

    def create_batch(self) -> tuple[TriageJobBatch | None, list[TriageJobBatchItem]]:
        return self._create_triage_job_batch_usecase.execute(CreateTriageJobBatchCommand())

    def process_batch(self, batch: TriageJobBatch, items: list[TriageJobBatchItem]) -> None:
        try:
            command = ProcessTriageJobBatchCommand(batch=batch, items=items)
            self._process_triage_job_batch_usecase.execute(command)
            _logger.execute(
                "info",
                "triage_batch_processed",
                batch_id=str(batch.id),
                total_items=batch.total_items,
            )
        except Exception:
            _logger.execute(
                "exception",
                "triage_batch_process_failed",
                batch_id=str(batch.id),
                total_items=batch.total_items,
            )
            raise
