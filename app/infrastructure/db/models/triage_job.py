from pydantic import UUID4
from sqlalchemy import Enum as SAEnum, UUID as PG_UUID, ForeignKey, INT
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.domain.enums.triage_job_status import TriageJobStatus
from .base_model import BaseModel

class TriageJobModel(BaseModel):
    __tablename__ = "triage_jobs"

    attempts: Mapped[int] = mapped_column(INT, nullable=False)
    ticket_id: Mapped[UUID4] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tickets.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    status: Mapped[TriageJobStatus] = mapped_column(SAEnum(
        TriageJobStatus,
        name="triage_job_status",
        native_enum=True,
    ), default=TriageJobStatus.PENDING)
    ticket = relationship(
        "TicketModel",
        back_populates="triage_jobs",
        lazy="select"
    )
    triage_job_logs = relationship(
        "TriageJobLogModel",
        back_populates="triage_job",
        cascade="all, delete, delete-orphan",
        lazy="select"
    )



