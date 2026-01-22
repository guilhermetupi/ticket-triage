from abc import ABC, abstractmethod
from typing import Any, Self


class UnitOfWorkGateway(ABC):
    session: Any | None

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc, tb) -> None:
        pass
