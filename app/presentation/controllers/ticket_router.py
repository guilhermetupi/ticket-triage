from fastapi import APIRouter

from app.infrastructure.di.presentation.ticket_controllers_container import TicketControllersContainer
from app.presentation.dtos.requests.create_ticket_request import CreateTicketRequest
from app.presentation.dtos.responses.ticket_response import TicketResponse

_ticket_controller = TicketControllersContainer().ticket_controller()

ticket_router = APIRouter(prefix='/tickets', tags=['Tickets'])

@ticket_router.post('/', response_model=TicketResponse, status_code=201)
def create_ticket(request: CreateTicketRequest):
    return _ticket_controller.create_ticket(request)


@ticket_router.post('/batch', status_code=207)
def create_ticket_batch(requests: list[CreateTicketRequest]):
    return _ticket_controller.create_ticket_batch(requests)
