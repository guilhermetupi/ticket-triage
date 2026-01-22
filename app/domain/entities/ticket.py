import uuid
from datetime import datetime
from dataclasses import dataclass
from app.domain.entities.base_entity import BaseEntity
from app.domain.enums.ticket_triage_status import TicketTriageStatus
from app.domain.exceptions.ticket_exception_code import TICKET_EXCEPTION
from app.domain.exceptions.unprocessable_entity_exception import UnprocessableEntityException


@dataclass(frozen=True)
class Ticket(BaseEntity):
    title: str
    description: str
    external_id: str
    owner_id: uuid.UUID
    triage_status: TicketTriageStatus = TicketTriageStatus.PENDING

    @staticmethod
    def create(
            title: str,
            description: str,
            external_id: str,
            owner_id: uuid.UUID,
            triage_status: TicketTriageStatus = TicketTriageStatus.PENDING,
    ):
        return Ticket(
            id=uuid.uuid4(),
            title=title,
            description=description,
            external_id=external_id,
            owner_id=owner_id,
            triage_status=triage_status,
        )

    @staticmethod
    def reconstitute(
            id: uuid.UUID,
            title: str,
            description: str,
            external_id: str,
            owner_id: uuid.UUID,
            triage_status: TicketTriageStatus,
            created_at: datetime,
            updated_at: datetime,
            deleted_at: datetime
    ):
        return Ticket(
            id=id,
            title=title,
            description=description,
            external_id=external_id,
            owner_id=owner_id,
            triage_status=triage_status,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

    def on_triage(self):
        if self.triage_status != TicketTriageStatus.PENDING:
            raise UnprocessableEntityException(
                **TICKET_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status":self.triage_status, "new_status":TicketTriageStatus.ON_TRIAGE}
            )
        data = {**self.__dict__, "triage_status": TicketTriageStatus.ON_TRIAGE}
        return Ticket.reconstitute(**data)

    def on_complete(self):
        if self.triage_status == TicketTriageStatus.PENDING:
            raise UnprocessableEntityException(
                **TICKET_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status":TicketTriageStatus.PENDING, "new_status":TicketTriageStatus.COMPLETED}
            )
        data = {**self.__dict__, "triage_status": TicketTriageStatus.COMPLETED}
        return Ticket.reconstitute(**data)
    def on_fail(self):
        if self.triage_status == TicketTriageStatus.COMPLETED:
            raise UnprocessableEntityException(
                **TICKET_EXCEPTION['INVALID_STATUS_CHANGE'],
                message_params={"actual_status": TicketTriageStatus.COMPLETED, "new_status": TicketTriageStatus.FAILED}
            )
        data = {**self.__dict__, "triage_status": TicketTriageStatus.FAILED}
        return Ticket.reconstitute(**data)
