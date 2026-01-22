from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions.common_exception_code import COMMON_EXCEPTION
from app.domain.exceptions.domain_exception import DomainException
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)


def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={
            "code": exc.code,
            "message": exc.message,
        },
    )


def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    if exc.status_code == 404:
        payload = COMMON_EXCEPTION["ROUTE_NOT_FOUND"]
        level = "warning"
    else:
        payload = COMMON_EXCEPTION["INTERNAL_SERVER_ERROR"]
        level = "exception" if exc.status_code >= 500 else "warning"

    _logger.execute(
        level,
        "http_exception",
        status_code=exc.status_code,
        method=request.method,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": payload["code"],
            "message": payload["message"],
        },
    )


def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    _logger.execute(
        "exception",
        "unhandled_exception",
        method=request.method,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": COMMON_EXCEPTION["INTERNAL_SERVER_ERROR"]["code"],
            "message": COMMON_EXCEPTION["INTERNAL_SERVER_ERROR"]["message"],
        },
    )
