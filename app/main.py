from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions.domain_exception import DomainException
from app.presentation.exception_handlers import (
    domain_exception_handler,
    http_exception_handler,
    unexpected_exception_handler,
)
from app.presentation.controllers.ticket_router import ticket_router
from app.presentation.controllers.triage_job_router import triage_job_router


def create_app() -> FastAPI:
    fast_api= FastAPI()

    fast_api.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origins=["*"],
    )

    fast_api.add_exception_handler(DomainException, domain_exception_handler)
    fast_api.add_exception_handler(StarletteHTTPException, http_exception_handler)
    fast_api.add_exception_handler(Exception, unexpected_exception_handler)
    fast_api.include_router(ticket_router)
    fast_api.include_router(triage_job_router)

    return fast_api

app = create_app()
