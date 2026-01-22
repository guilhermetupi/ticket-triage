from app.domain.entities.triage_job_batch import TriageJobBatch
from app.domain.enums.triage_job_batch_status import TriageJobBatchStatus
from app.infrastructure.db.models import TriageJobBatchModel


class TriageJobBatchMapper:
    @staticmethod
    def to_model(entity: TriageJobBatch) -> TriageJobBatchModel:
        return TriageJobBatchModel(
            id=entity.id,
            status=entity.status,
            total_items=entity.total_items,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_entity(model: TriageJobBatchModel) -> TriageJobBatch:
        return TriageJobBatch.reconstitute(
            id=model.id,
            status=TriageJobBatchStatus(model.status),
            total_items=model.total_items,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
