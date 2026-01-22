from abc import ABC, abstractmethod


class LLMClientGateway(ABC):
    @abstractmethod
    def execute(self, *, system: str, user: str, temperature: float, max_tokens: int) -> str:
        pass
