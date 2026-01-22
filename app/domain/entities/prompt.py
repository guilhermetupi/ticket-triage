import uuid
from datetime import datetime
from dataclasses import dataclass
from app.domain.entities.base_entity import BaseEntity


@dataclass(frozen=True)
class Prompt(BaseEntity):
    name: str
    version: str
    owner_id: uuid.UUID | None
    system_prompt: str
    input_schema: dict[str, str]
    output_schema: dict[str, str]
    user_template: str
    invariants: dict[str, str]
    active: bool
    default: bool

    @staticmethod
    def create(
            name: str,
            version: str,
            owner_id: uuid.UUID | None,
            system_prompt: str,
            input_schema: dict[str, str],
            output_schema: dict[str, str],
            user_template: str,
            invariants: dict[str, str],
            active: bool,
            default: bool,
    ):
        return Prompt(
            id=uuid.uuid4(),
            name=name,
            version=version,
            owner_id=owner_id,
            system_prompt=system_prompt,
            input_schema=input_schema,
            output_schema=output_schema,
            user_template=user_template,
            invariants=invariants,
            active=active,
            default=default,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            name: str,
            version: str,
            owner_id: uuid.UUID | None,
            system_prompt: str,
            input_schema: dict[str, str],
            output_schema: dict[str, str],
            user_template: str,
            invariants: dict[str, str],
            active: bool,
            default: bool,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime
    ):
        return Prompt(
            id=id,
            name=name,
            version=version,
            owner_id=owner_id,
            system_prompt=system_prompt,
            input_schema=input_schema,
            output_schema=output_schema,
            user_template=user_template,
            invariants=invariants,
            active=active,
            default=default,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )
