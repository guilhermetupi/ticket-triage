from app.domain.entities.prompt import Prompt
from app.infrastructure.db.models import PromptModel


class PromptMapper:
    @staticmethod
    def to_model(entity: Prompt) -> PromptModel:
        return PromptModel(
            id=entity.id,
            name=entity.name,
            version=entity.version,
            owner_id=entity.owner_id,
            system_prompt=entity.system_prompt,
            user_template=entity.user_template,
            input_schema=entity.input_schema,
            output_schema=entity.output_schema,
            invariants=entity.invariants,
            active=entity.active,
            default=entity.default,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_entity(model: PromptModel) -> Prompt:
        return Prompt.reconstitute(
            id=model.id,
            name=model.name,
            version=model.version,
            owner_id=model.owner_id,
            system_prompt=model.system_prompt,
            user_template=model.user_template,
            input_schema=model.input_schema,
            output_schema=model.output_schema,
            invariants=model.invariants,
            active=model.active,
            default=model.default,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
