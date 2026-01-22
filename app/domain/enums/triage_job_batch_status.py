from enum import Enum


class TriageJobBatchStatus(str, Enum):
    RUNNING = "RUNNING"
    DONE = "DONE"
