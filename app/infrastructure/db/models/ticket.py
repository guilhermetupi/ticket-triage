from pydantic import UUID4
from sqlalchemy import String, Text, Enum as SAEnum, UUID as PG_UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.enums.ticket_triage_status import TicketTriageStatus
from .base_model import BaseModel

class TicketModel(BaseModel):
    __tablename__ = "tickets"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    owner_id: Mapped[UUID4] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    triage_status: Mapped[TicketTriageStatus] = mapped_column(SAEnum(
        TicketTriageStatus,
        name="triage_status",
        native_enum=True,
    ), default=TicketTriageStatus.PENDING)
    owner = relationship(
        "OwnerModel",
        back_populates="tickets",
        lazy="select"
    )
    triage_jobs = relationship(
        "TriageJobModel",
        back_populates="ticket",
        cascade="all, delete, delete-orphan",
        lazy="select"
    )



