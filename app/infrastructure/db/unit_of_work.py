from __future__ import annotations

from typing import Callable

from sqlalchemy.orm import Session, sessionmaker

from app.domain.gateways.unit_of_work_gateway import UnitOfWorkGateway


class SqlAlchemyUnitOfWork(UnitOfWorkGateway):
    """
    UoW simples:
    - abre Session
    - begin transaction
    - commit se ok
    - rollback se exception
    - close sempre
    """

    def __init__(self, session_factory: sessionmaker | Callable[[], Session]):
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.session.begin()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None
