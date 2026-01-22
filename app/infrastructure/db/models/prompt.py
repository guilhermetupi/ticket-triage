from pydantic import UUID4
from sqlalchemy import String, Text, Boolean, UniqueConstraint, ForeignKey, UUID as PG_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped
from .base_model import BaseModel

class PromptModel(BaseModel):
    __tablename__ = "prompts"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[UUID4 | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id", ondelete="SET NULL", onupdate="CASCADE"),
        index=True,
        nullable=True,
    )
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_template: Mapped[str] = mapped_column(Text, nullable=False)
    input_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    output_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    invariants: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint("name", "version", "owner_id", name="prompt_name_version_owner"),
    )
