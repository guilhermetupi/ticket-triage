import uuid
from datetime import datetime
from dataclasses import dataclass
from app.domain.entities.base_entity import BaseEntity


@dataclass(frozen=True)
class Owner(BaseEntity):
    name: str
    webhook_url: str

    @staticmethod
    def create(
            name: str,
            webhook_url: str,
    ):
        return Owner(
            id=uuid.uuid4(),
            name=name,
            webhook_url=webhook_url,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            name: str,
            webhook_url: str,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime
    ):
        return Owner(
            id=id,
            name=name,
            webhook_url=webhook_url,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )