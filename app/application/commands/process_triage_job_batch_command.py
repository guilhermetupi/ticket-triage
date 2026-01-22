from pydantic import BaseModel, ConfigDict

from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.entities.triage_job_batch_item import TriageJobBatchItem


class ProcessTriageJobBatchCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    batch: TriageJobBatch
    items: list[TriageJobBatchItem]
