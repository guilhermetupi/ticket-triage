from enum import Enum

class TicketTriageStatus(str, Enum):
    PENDING = "PENDING"
    ON_TRIAGE = "ON_TRIAGE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"