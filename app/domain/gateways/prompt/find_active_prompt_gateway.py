import uuid
from abc import ABC, abstractmethod

from app.domain.entities.prompt import Prompt


class FindActivePromptGateway(ABC):
    @abstractmethod
    def execute(self, name: str, owner_id: uuid.UUID | None = None) -> Prompt | None:
        pass
