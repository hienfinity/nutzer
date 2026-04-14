"""Minimale FastAPI-Anwendung fuer den Anfangszustand des Projekts."""

from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Final

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from nutzer.config import config_logger
from nutzer.graphql_api import graphql_router
from nutzer.problem_details import create_problem_details
from nutzer.router.nutzer_router import nutzer_router
from nutzer.router.nutzer_write_router import nutzer_write_router
from nutzer.router.shutdown_router import router as shutdown_router
from nutzer.security import AuthorizationError, LoginError, set_response_headers
from nutzer.security import router as auth_router
from nutzer.service import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)

__all__ = ["app"]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Logging beim Start vorbereiten."""
    Path("log").mkdir(exist_ok=True)
    config_logger()
    yield


app: Final = FastAPI(
    title="Nutzer",
    description="Technisches Grundgeruest fuer das Nutzer-Projekt",
    version="2026.4.1",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.include_router(nutzer_router, prefix="/rest")
app.include_router(nutzer_write_router, prefix="/rest")
app.include_router(auth_router, prefix="/auth")
app.include_router(graphql_router, prefix="/graphql")
app.include_router(shutdown_router)


@app.get("/")
def index() -> dict[str, str]:
    """Einfacher Startendpunkt fuer den Anfangszustand."""
    return {"message": "Nutzer-Projekt gestartet"}


@app.get("/health")
def health() -> dict[str, str]:
    """Einfacher Health-Check ohne Datenbankzugriff."""
    return {"status": "up"}


@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Security-Header auf jede Antwort setzen."""
    response = await call_next(request)
    set_response_headers(response)
    return response


@app.exception_handler(AuthorizationError)
def authorization_error_handler(
    _request: Request,
    _err: AuthorizationError,
) -> Response:
    """ProblemDetails fuer fehlerhafte oder fehlende Authorisierung zurueckgeben."""
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(LoginError)
def login_error_handler(_request: Request, err: LoginError) -> Response:
    """ProblemDetails fuer fehlerhafte Login-Daten zurueckgeben."""
    return create_problem_details(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(err),
    )


@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """ProblemDetails fuer nicht gefundene Ressourcen zurueckgeben."""
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(EmailExistsError)
def email_exists_error_handler(
    _request: Request,
    err: EmailExistsError,
) -> Response:
    """ProblemDetails fuer doppelte Emailadressen zurueckgeben."""
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(UsernameExistsError)
def username_exists_error_handler(
    _request: Request,
    err: UsernameExistsError,
) -> Response:
    """ProblemDetails fuer doppelte Benutzernamen zurueckgeben."""
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """ProblemDetails fuer veraltete Versionsnummern zurueckgeben."""
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )
