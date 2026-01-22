from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class UpdateTicketTriageStatusGateway(ABC):
    @abstractmethod
    def execute(self, ticket: Ticket) -> Ticket | None:
        pass
