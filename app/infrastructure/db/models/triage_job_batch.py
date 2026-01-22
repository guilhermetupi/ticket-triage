from sqlalchemy import Enum as SAEnum, INT
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.enums.triage_job_batch_status import TriageJobBatchStatus
from .base_model import BaseModel


class TriageJobBatchModel(BaseModel):
    __tablename__ = "triage_job_batches"

    status: Mapped[TriageJobBatchStatus] = mapped_column(SAEnum(
        TriageJobBatchStatus,
        name="triage_job_batch_status",
        native_enum=True,
    ), nullable=False)
    total_items: Mapped[int] = mapped_column(INT, nullable=False)
    batch_items = relationship(
        "TriageJobBatchItemModel",
        back_populates="batch",
        cascade="all, delete, delete-orphan",
        lazy="select",
    )
