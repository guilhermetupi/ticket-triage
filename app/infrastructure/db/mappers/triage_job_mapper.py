from app.domain.entities.triage_job import TriageJob
from app.infrastructure.db.models import TriageJobModel


class TriageJobMapper:
    @staticmethod
    def to_model(entity: TriageJob) -> TriageJobModel:
        return TriageJobModel(
            id=entity.id,
            ticket_id=entity.ticket_id,
            status=entity.status,
            attempts=entity.attempts,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_entity(model: TriageJobModel) -> TriageJob:
        return TriageJob.reconstitute(
            id=model.id,
            ticket_id=model.ticket_id,
            status=model.status,
            attempts=model.attempts,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
