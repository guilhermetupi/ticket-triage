from app.domain.exceptions.domain_exception import DomainException


class UnprocessableEntityException(DomainException):
    def __init__(self, message: str = None, code: str = None, message_params: dict[str, object] | None = None) -> None:
        super().__init__(message=message.format(**message_params), code=code, status=422)