from dependency_injector import containers, providers
from app.infrastructure.llm.client import OllamaClient


class TicketDatabaseRepositoriesContainer(containers.DeclarativeContainer):
    llm_client = providers.Factory(OllamaClient)
