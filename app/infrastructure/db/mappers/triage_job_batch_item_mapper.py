from app.domain.entities.triage_job_batch_item import TriageJobBatchItem
from app.infrastructure.db.models import TriageJobBatchItemModel


class TriageJobBatchItemMapper:
    @staticmethod
    def to_model(entity: TriageJobBatchItem) -> TriageJobBatchItemModel:
        return TriageJobBatchItemModel(
            id=entity.id,
            batch_id=entity.batch_id,
            triage_job_id=entity.triage_job_id,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_entity(model: TriageJobBatchItemModel) -> TriageJobBatchItem:
        return TriageJobBatchItem.reconstitute(
            id=model.id,
            batch_id=model.batch_id,
            triage_job_id=model.triage_job_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
