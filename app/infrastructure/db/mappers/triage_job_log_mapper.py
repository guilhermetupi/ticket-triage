from app.domain.entities.triage_job_log import TriageJobLog
from app.infrastructure.db.models import TriageJobLogModel


class TriageJobLogMapper:
    @staticmethod
    def to_model(entity: TriageJobLog) -> TriageJobLogModel:
        return TriageJobLogModel(
            id=entity.id,
            success=entity.success,
            input=entity.input,
            output=entity.output,
            prompt_id=entity.prompt_id,
            triage_job_id=entity.triage_job_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_entity(model: TriageJobLogModel) -> TriageJobLog:
        return TriageJobLog.reconstitute(
            id=model.id,
            success=model.success,
            input=model.input,
            output=model.output,
            prompt_id=model.prompt_id,
            triage_job_id=model.triage_job_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
