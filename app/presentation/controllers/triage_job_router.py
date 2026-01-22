from fastapi import APIRouter, BackgroundTasks, status

from app.infrastructure.di.presentation.triage_job_controllers_container import (
    TriageJobControllersContainer,
)

_triage_job_controller = TriageJobControllersContainer().triage_job_controller()

triage_job_router = APIRouter(prefix="/triage-jobs", tags=["Triage Jobs"])


@triage_job_router.post("/batch", status_code=status.HTTP_202_ACCEPTED)
def create_triage_batch(background_tasks: BackgroundTasks):
    batch, items = _triage_job_controller.create_batch()
    if batch is None:
        return {"status": "EMPTY", "batch": None, "total_items": 0}
    background_tasks.add_task(_triage_job_controller.process_batch, batch, items)
    return {
        "status": "QUEUED",
        "batch": {
            "id": str(batch.id),
            "total_items": batch.total_items,
        },
    }
