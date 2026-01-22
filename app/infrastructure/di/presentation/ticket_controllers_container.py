from dependency_injector import providers, containers

from app.infrastructure.di.application.ticket_usecases_container import TicketUseCasesContainer
from app.presentation.controllers.ticket_controller import TicketController


class TicketControllersContainer(containers.DeclarativeContainer):
    ticket_usecases_container = providers.Container(TicketUseCasesContainer)
    ticket_controller = providers.Factory(
        TicketController,
        create_ticket_usecase=ticket_usecases_container.create_ticket_usecase,
    )
