import json
import logging
import os
from datetime import datetime, UTC
from typing import Any

from app.domain.gateways.logger_gateway import LoggerGateway


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        context = getattr(record, "context", None)
        if isinstance(context, dict):
            payload.update(context)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


_CONFIGURED = False


def _configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    base_logger = logging.getLogger("app")
    base_logger.setLevel(level)
    if not base_logger.handlers:
        base_logger.addHandler(handler)
    base_logger.propagate = False
    _CONFIGURED = True


class StructuredLogger(LoggerGateway):
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def execute(self, level: str, message: str, **context: Any) -> None:
        level_key = level.lower()
        if level_key == "info":
            self._logger.info(message, extra={"context": context})
            return
        if level_key == "warning":
            self._logger.warning(message, extra={"context": context})
            return
        if level_key == "error":
            self._logger.error(message, extra={"context": context})
            return
        if level_key == "exception":
            self._logger.exception(message, extra={"context": context})
            return
        raise ValueError(f"Unsupported log level: {level}")


def get_logger(name: str) -> LoggerGateway:
    _configure_logging()
    return StructuredLogger(logging.getLogger(f"app.{name}"))
