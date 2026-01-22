from pydantic import UUID4
from sqlalchemy import UUID as PG_UUID, ForeignKey, Boolean, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base_model import BaseModel

class TriageJobLogModel(BaseModel):
    __tablename__ = "triage_job_logs"

    input: Mapped[str] = mapped_column(Text, nullable=False)
    output: Mapped[str] = mapped_column(Text, nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    prompt_id: Mapped[UUID4 | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=True,
    )
    prompt = relationship(
        "PromptModel",
        lazy="select"
    )
    triage_job_id: Mapped[UUID4] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("triage_jobs.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    triage_job = relationship(
        "TriageJobModel",
        back_populates="triage_job_logs",
        lazy="select"
    )

