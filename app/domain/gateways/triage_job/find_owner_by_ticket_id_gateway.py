from abc import ABC, abstractmethod
import uuid

from app.domain.entities.owner import Owner


class FindOwnerByIdGateway(ABC):
    @abstractmethod
    def execute(self, id: uuid.UUID) -> Owner | None:
        pass
