import uuid
from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.create_triage_job_command import CreateTriageJobCommand
from app.application.transactional import transactional
from app.domain.entities.triage_job import TriageJob
from app.domain.exceptions.conflict_exception import ConflictException
from app.domain.exceptions.ticket_exception_code import TICKET_EXCEPTION
from app.domain.gateways.triage_job.create_triage_job_gateway import CreateTriageJobGateway
from app.domain.gateways.triage_job.find_triage_job_by_id_gateway import FindTriageJobByTicketIdGateway
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)


class CreateTriageJobUseCase:
    def __init__(
            self,
            uow,
            create_triage_job_gateway: Callable[[Session], CreateTriageJobGateway],
            find_triage_job_by_ticket_id_gateway: Callable[[Session], FindTriageJobByTicketIdGateway],
    ):
        self.uow = uow
        self._create_triage_job_gateway = create_triage_job_gateway
        self._find_triage_job_by_ticket_id = find_triage_job_by_ticket_id_gateway

    @transactional
    def execute(self, command: CreateTriageJobCommand, *, db: Session | None = None) -> TriageJob:
        assert db is not None
        _logger.execute("info", "triage_job_create_started", ticket_id=str(command.ticket_id))
        self._validate_triage_job(command.ticket_id, db)
        triage_job = TriageJob.create(command.ticket_id)
        triage_job = self._create_triage_job_gateway(db).execute(triage_job)
        _logger.execute(
            "info",
            "triage_job_created",
            triage_job_id=str(triage_job.id),
            ticket_id=str(triage_job.ticket_id),
        )
        return triage_job

    def _validate_triage_job(self, ticket_id: uuid.UUID, db: Session) -> None:
        triage_job_exists = self._find_triage_job_by_ticket_id(db).execute(ticket_id)
        if triage_job_exists:
            _logger.execute(
                "warning",
                "triage_job_create_conflict",
                ticket_id=str(ticket_id),
                triage_job_id=str(triage_job_exists.id),
            )
            raise ConflictException(
                **TICKET_EXCEPTION['TICKET_ALREADY_EXISTS'],
                message_params={"id":ticket_id, "triage_job_id":triage_job_exists.id}
            )
