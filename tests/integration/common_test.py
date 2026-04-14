"""Allgemeine Daten fuer die Tests."""

from collections.abc import Mapping
from datetime import date
from typing import Any, Final

from fastapi.testclient import TestClient

from nutzer.entity import Adresse, Einstellung, Interesse, Nutzer, Rolle, Status
from nutzer.fastapi_app import app
from nutzer.repository import Pageable, Slice
from nutzer.router.dependencies import get_service, get_write_service
from nutzer.security.dependencies import get_token_service
from nutzer.security.exceptions import LoginError
from nutzer.security.role import Role
from nutzer.security.user import User
from nutzer.service import (
    EmailExistsError,
    NotFoundError,
    NutzerDTO,
    UsernameExistsError,
    VersionOutdatedError,
)

__all__ = [
    "base_url",
    "check_readiness",
    "ctx",
    "db_populate",
    "db_populate_path",
    "delete",
    "get",
    "graphql_path",
    "graphql_url",
    "health_url",
    "keycloak_populate",
    "keycloak_populate_path",
    "login",
    "password_admin",
    "post",
    "put",
    "rest_path",
    "rest_url",
    "timeout",
    "token_path",
    "username_admin",
]

schema: Final = "http"
port: Final = 80
host: Final = "testserver"
base_url: Final = f"{schema}://{host}"
rest_path: Final = "/rest"
rest_url: Final = f"{base_url}{rest_path}"
health_url: Final = f"{base_url}/health"
graphql_path: Final = "/graphql"
graphql_url: Final = f"{base_url}{graphql_path}"
token_path: Final = "/auth/token"
db_populate_path: Final = "/dev/db_populate"
keycloak_populate_path: Final = "/dev/keycloak_populate"
username_admin: Final = "admin"
password_admin: Final = "p"  # NOSONAR
timeout: Final = 2
ctx = None
