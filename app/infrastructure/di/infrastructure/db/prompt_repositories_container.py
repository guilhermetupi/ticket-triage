from dependency_injector import containers, providers

from app.infrastructure.db.repositories.prompt.find_active_prompt_repository import (
    SqlAlchemyFindActivePromptRepository,
)


class PromptDatabaseRepositoriesContainer(containers.DeclarativeContainer):
    find_active_prompt = providers.Factory(SqlAlchemyFindActivePromptRepository)
