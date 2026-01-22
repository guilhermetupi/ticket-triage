from abc import ABC, abstractmethod
from typing import Any


class LoggerGateway(ABC):
    @abstractmethod
    def execute(self, level: str, message: str, **context: Any) -> None:
        pass
