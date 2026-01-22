from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class CreateTicketGateway(ABC):
    @abstractmethod
    def execute(self, ticket: Ticket) -> Ticket:
        pass

