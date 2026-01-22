# AGENTS.md

These are the project rules for any agent modifying this repository. Follow them
exactly and keep changes consistent with existing patterns.

## Core Architecture Rules
- Classes (except controllers) must have only one public method: `execute`.
- Every use case parameter must be a Command object (no raw primitives).
- Every service/repository/infra class must implement a Gateway interface.
- Entities must enforce business rules when mutating state.
- Repositories must return Entities (never ORM models).
- DB mappers must be classes with static methods (`to_model`, `to_entity`).

Example:
```python
class ExampleUseCase:
    def execute(self, command: ExampleCommand) -> None:
        ...
```
```python
# Wrong: extra public methods
class ExampleUseCase:
    def execute(self, command: ExampleCommand) -> None:
        ...
    def helper(self) -> None:
        ...
```

## Use Cases
- Public API: `execute(command, ...)` only.
- Use cases should never expose additional public helpers.
- Commands live in `app/application/commands` and should be the only input type.

Example:
```python
class CreateTicketUseCase:
    def execute(self, command: CreateTicketCommand) -> Ticket:
        ...
```
```python
# Wrong: raw params instead of a command
def execute(self, owner_id: UUID, title: str) -> Ticket:
    ...
```

## Gateways & Infra
- Define a Gateway in `app/domain/gateways` before implementing infra classes.
- Infra classes must implement the corresponding Gateway.
- Keep infra implementations focused on I/O; business rules belong in Entities.

Example:
```python
class FindTicketByIdGateway(ABC):
    @abstractmethod
    def execute(self, ticket_id: UUID) -> Ticket | None:
        ...
```
```python
class SqlAlchemyFindTicketByIdRepository(FindTicketByIdGateway):
    def execute(self, ticket_id: UUID) -> Ticket | None:
        ...
```

## Entities
- All state transitions must go through entity methods (ex: `on_running`).
- Enforce invariants and invalid transitions via domain exceptions.
- Never update entity state directly in repositories or use cases.

Example:
```python
ticket = ticket.on_triage()
```
```python
# Wrong: direct mutation
ticket.triage_status = TicketTriageStatus.ON_TRIAGE
```

## Repositories
- Return entities for all read/write operations.
- Do not leak ORM models outside repositories.
- Use mappers for all entity/model conversions.

Example:
```python
model = self._db.get(TicketModel, ticket_id)
return TicketMapper.to_entity(model)
```
```python
# Wrong: returning ORM model
return model
```

## Mappers
- Must be classes with static methods only:
  - `to_model(entity)`
  - `to_entity(model)`

Example:
```python
class TicketMapper:
    @staticmethod
    def to_model(entity: Ticket) -> TicketModel:
        ...
```

## Transactions
- When using `@transactional`, do not inject DB sessions elsewhere.
- Use Unit of Work for commit/rollback boundaries.

Example:
```python
@transactional
def execute(self, command: ExampleCommand, *, db: Session | None = None) -> None:
    assert db is not None
```
```python
# Wrong: session injected outside transactional boundary
def execute(self, command: ExampleCommand, db: Session) -> None:
    ...
```
