from app.domain.exceptions.domain_exception import DomainException


class ConflictException(DomainException):
    def __init__(self, message: str = None, code: str = None, message_params: dict[str, object] | None = None) -> None:
        if message_params is None:
            message_params = {}
        super().__init__(message=message.format(**message_params), code=code, status=409)
