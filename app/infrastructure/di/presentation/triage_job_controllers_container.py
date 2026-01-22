from dependency_injector import providers, containers

from app.infrastructure.di.application.triage_job_usecases_container import TriageJobUseCasesContainer
from app.presentation.controllers.triage_job_controller import TriageJobController


class TriageJobControllersContainer(containers.DeclarativeContainer):
    triage_job_usecases_container = providers.Container(TriageJobUseCasesContainer)
    triage_job_controller = providers.Factory(
        TriageJobController,
        create_triage_job_batch_usecase=triage_job_usecases_container.create_triage_job_batch_usecase,
        process_triage_job_batch_usecase=triage_job_usecases_container.process_triage_job_batch_usecase,
    )
