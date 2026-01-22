import uuid
from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class FindTicketByIdGateway(ABC):
    @abstractmethod
    def execute(self, ticket_id: uuid.UUID) -> Ticket | None:
        pass
