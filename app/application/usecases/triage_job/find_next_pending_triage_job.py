from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.find_next_pending_triage_job_command import FindNextPendingTriageJobCommand
from app.application.transactional import transactional
from app.domain.entities.triage_job import TriageJob
from app.domain.gateways.triage_job.find_next_pending_triage_job_gateway import FindNextPendingTriageJobDatabaseGateway


class FindNextPendingTriageJobUseCase:
    def __init__(
            self,
            uow,
            find_next_pending_triage_job_gateway: Callable[[Session], FindNextPendingTriageJobDatabaseGateway],
    ):
        self.uow = uow
        self._find_next_pending_triage_job_gateway = find_next_pending_triage_job_gateway

    @transactional
    def execute(
            self,
            command: FindNextPendingTriageJobCommand,
            *,
            db: Session | None = None,
    ) -> TriageJob | None:
        assert db is not None
        return self._find_next_pending_triage_job_gateway(db).execute()
