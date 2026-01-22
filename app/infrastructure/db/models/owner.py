from pydantic import UUID4
from sqlalchemy import String, Text, Enum as SAEnum, UUID as PG_UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.enums.ticket_triage_status import TicketTriageStatus
from .base_model import BaseModel

class OwnerModel(BaseModel):
    __tablename__ = "owners"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    webhook_url: Mapped[str] = mapped_column(String(255), nullable=False)
    tickets = relationship(
        "TicketModel",
        back_populates="owner",
        cascade="all, delete, delete-orphan",
        lazy="select"
    )

