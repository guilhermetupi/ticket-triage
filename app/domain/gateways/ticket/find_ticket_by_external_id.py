from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class FindTicketByExternalIdGateway(ABC):
    @abstractmethod
    def execute(self, external_id: str) -> Ticket | None:
        pass
