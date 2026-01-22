import httpx
from dataclasses import dataclass
from app.config.settings import settings
from app.domain.gateways.llm_client_gateway import LLMClientGateway


@dataclass
class OllamaClient(LLMClientGateway):
    _base_url: str = settings.LLM_BASE_URL
    _model: str = settings.LLM_MODEL

    def execute(self, *, system: str, user: str, temperature: float, max_tokens: int) -> str:
        payload = self._make_payload(system=system, user=user, temperature=temperature, max_tokens=max_tokens)

        with httpx.Client(timeout=60.0) as client:
            r = client.post(self._base_url, json=payload)
            r.raise_for_status()
            data = r.json()

        return data["message"]["content"]

    def _make_payload(self, *, system: str, user: str, temperature: float, max_tokens: int) -> dict:
        return {
            "model": self._model,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predicts": max_tokens,
            },
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
