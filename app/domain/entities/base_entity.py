import uuid
from datetime import datetime, UTC
from dataclasses import field, dataclass

@dataclass(frozen=True, kw_only=True)
class BaseEntity:
    id: uuid.UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None
