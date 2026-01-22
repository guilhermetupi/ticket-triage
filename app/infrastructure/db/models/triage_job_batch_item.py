from pydantic import UUID4
from sqlalchemy import Enum as SAEnum, UUID as PG_UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.enums.triage_job_status import TriageJobStatus
from .base_model import BaseModel


class TriageJobBatchItemModel(BaseModel):
    __tablename__ = "triage_job_batch_items"

    batch_id: Mapped[UUID4] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("triage_job_batches.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    triage_job_id: Mapped[UUID4] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("triage_jobs.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    status: Mapped[TriageJobStatus] = mapped_column(SAEnum(
        TriageJobStatus,
        name="triage_job_status",
        native_enum=True,
    ), default=TriageJobStatus.PENDING)
    batch = relationship(
        "TriageJobBatchModel",
        back_populates="batch_items",
        lazy="select",
    )
    triage_job = relationship(
        "TriageJobModel",
        lazy="select",
    )
