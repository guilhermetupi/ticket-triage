from app.application.commands.create_ticket_command import CreateTicketCommand
from app.application.usecases.ticket.create_ticket_usecase import CreateTicketUseCase
from app.domain.exceptions.domain_exception import DomainException
from app.infrastructure.logging import get_logger
from app.presentation.dtos.requests.create_ticket_request import CreateTicketRequest
from app.presentation.dtos.responses.ticket_response import TicketResponse


_logger = get_logger(__name__)


class TicketController:
    def __init__(self, create_ticket_usecase: CreateTicketUseCase):
        self.create_ticket_usecase = create_ticket_usecase

    def create_ticket(self, create_ticket_request: CreateTicketRequest) -> TicketResponse:
        _logger.execute(
            "info",
            "ticket_create_request_received",
            external_id=create_ticket_request.external_id,
            owner_id=create_ticket_request.owner_id,
            title=create_ticket_request.title,
            description_length=len(create_ticket_request.description),
        )
        create_ticket_command = CreateTicketCommand(**create_ticket_request.__dict__)
        ticket = self.create_ticket_usecase.execute(create_ticket_command)
        return TicketResponse(**ticket.__dict__)

    def create_ticket_batch(self, create_ticket_requests: list[CreateTicketRequest]) -> dict:
        results: list[dict] = []
        for item in create_ticket_requests:
            try:
                create_ticket_command = CreateTicketCommand(**item.__dict__)
                ticket = self.create_ticket_usecase.execute(create_ticket_command)
                results.append(
                    {
                        "status": "CREATED",
                        "ticket_id": str(ticket.id),
                        "external_id": ticket.external_id,
                        "owner_id": str(ticket.owner_id),
                    }
                )
            except DomainException as exc:
                results.append(
                    {
                        "status": "FAILED",
                        "external_id": item.external_id,
                        "owner_id": str(item.owner_id),
                        "error": {
                            "code": exc.code,
                            "message": exc.message,
                            "status": exc.status,
                        },
                    }
                )
            except Exception as exc:
                _logger.execute(
                    "exception",
                    "ticket_create_batch_failed",
                    external_id=item.external_id,
                    owner_id=item.owner_id,
                )
                results.append(
                    {
                        "status": "FAILED",
                        "external_id": item.external_id,
                        "owner_id": str(item.owner_id),
                        "error": {
                            "code": "UNKNOWN",
                            "message": str(exc),
                            "status": 500,
                        },
                    }
                )

        return {"results": results}
