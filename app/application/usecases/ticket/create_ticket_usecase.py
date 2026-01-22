from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.create_ticket_command import CreateTicketCommand
from app.application.commands.create_triage_job_command import CreateTriageJobCommand
from app.application.transactional import transactional
from app.application.usecases.triage_job.create_triage_job import CreateTriageJobUseCase
from app.domain.entities.ticket import Ticket
from app.domain.exceptions.conflict_exception import ConflictException
from app.domain.exceptions.ticket_exception_code import TICKET_EXCEPTION
from app.domain.gateways.ticket.create_ticket_gateway import CreateTicketGateway
from app.domain.gateways.ticket.find_ticket_by_external_id import FindTicketByExternalIdGateway
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)


class CreateTicketUseCase:
    def __init__(
            self,
            uow,
            create_ticket_database_gateway: Callable[[Session], CreateTicketGateway],
            find_ticket_by_external_id: Callable[[Session], FindTicketByExternalIdGateway],
            create_triage_job_usecase: CreateTriageJobUseCase,
    ):
        self.uow = uow
        self._create_ticket_database_gateway = create_ticket_database_gateway
        self._find_ticket_by_external_id = find_ticket_by_external_id
        self._create_triage_job_usecase = create_triage_job_usecase

    @transactional
    def execute(self, command: CreateTicketCommand, *, db: Session | None = None) -> Ticket:
        assert db is not None
        _logger.execute(
            "info",
            "ticket_create_started",
            external_id=command.external_id,
            owner_id=command.owner_id,
        )
        ticket = Ticket.create(**command.__dict__)
        self._validate_ticket(ticket, db)

        ticket = self._create_ticket_database_gateway(db).execute(ticket)
        _logger.execute(
            "info",
            "ticket_created",
            ticket_id=ticket.id,
            external_id=ticket.external_id,
            owner_id=ticket.owner_id,
            triage_status=ticket.triage_status,
        )
        _logger.execute(
            "info",
            "triage_job_create_started",
            ticket_id=ticket.id,
        )
        self._create_triage_job_usecase.execute(
            CreateTriageJobCommand(ticket_id=ticket.id),
            db=db,
        )
        _logger.execute(
            "info",
            "triage_job_created",
            ticket_id=ticket.id,
        )

        return ticket

    def _validate_ticket(self, ticket: Ticket, db: Session) -> None:
        ticket_exists = self._find_ticket_by_external_id(db).execute(ticket.external_id)
        if ticket_exists:
            _logger.execute(
                "warning",
                "ticket_create_conflict",
                external_id=ticket.external_id,
                owner_id=ticket.owner_id,
            )
            raise ConflictException(**TICKET_EXCEPTION['ALREADY_EXISTS'], message_params={"external_id":ticket.external_id})
