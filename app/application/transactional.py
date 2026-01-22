from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")


def transactional(fn: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator para UseCase.execute(...)

    Requisitos:
    - O use case tem atributo self.uow (SqlAlchemyUnitOfWork ou factory)
    - O metodo decorado aceita parametro nomeado db (Session) opcional

    Comportamento:
    - abre transacao
    - injeta db
    - commit/rollback automatico via UoW
    """

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if kwargs.get("db") is not None:
            return fn(*args, **kwargs)

        self = args[0]
        uow = getattr(self, "uow", None)
        if uow is None:
            raise RuntimeError("UseCase sem self.uow (necessario para @transactional)")

        if not hasattr(uow, "__enter__"):
            if callable(uow):
                uow = uow()
            else:
                raise RuntimeError("self.uow nao eh um Unit of Work valido")

        with uow as active_uow:
            kwargs["db"] = active_uow.session
            return fn(*args, **kwargs)

    return cast(Callable[P, R], wrapper)
