import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.prompt import Prompt
from app.domain.gateways.prompt.find_active_prompt_gateway import FindActivePromptGateway
from app.infrastructure.db.mappers.prompt_mapper import PromptMapper
from app.infrastructure.db.models import PromptModel


class SqlAlchemyFindActivePromptRepository(FindActivePromptGateway):
    def __init__(self, db: Session):
        self._db = db

    def execute(self, name: str, owner_id: uuid.UUID | None = None) -> Prompt | None:
        base_filters = [
            PromptModel.name == name,
            PromptModel.active.is_(True),
            PromptModel.deleted_at.is_(None),
        ]

        if owner_id is not None:
            owner_stmt = (
                select(PromptModel)
                .where(*base_filters, PromptModel.owner_id == owner_id)
                .order_by(PromptModel.created_at.desc())
                .limit(1)
            )
            model = self._db.execute(owner_stmt).scalar_one_or_none()
            if model is not None:
                return PromptMapper.to_entity(model)

        default_stmt = (
            select(PromptModel)
            .where(*base_filters, PromptModel.default.is_(True))
            .order_by(PromptModel.created_at.desc())
            .limit(1)
        )
        model = self._db.execute(default_stmt).scalar_one_or_none()
        if model is None:
            return None
        return PromptMapper.to_entity(model)
