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


def _create_nutzer_dto(
    *,
    nutzer_id: int,
    version: int,
    vorname: str,
    nachname: str,
    email: str,
    username: str,
) -> NutzerDTO:
    nutzer = Nutzer(
        id=nutzer_id,
        version=version,
        vorname=vorname,
        nachname=nachname,
        email=email,
        username=username,
        telefonnummer="+49 721 123456",
        geburtsdatum=date(1995, 5, 17),
        beitrittsdatum=date(2024, 4, 1),
        aktiv=True,
        rolle=Rolle.NUTZER,
        status=Status.AKTIV,
        interessen=[Interesse.TECHNIK, Interesse.MUSIK],
        adresse=None,
        einstellung=None,
        erzeugt=None,
        aktualisiert=None,
    )
    nutzer.adresse = Adresse(
        id=100 + nutzer_id,
        nutzer_id=nutzer_id,
        strasse="Hauptstrasse",
        hausnummer="1a",
        plz="76133",
        ort="Karlsruhe",
        nutzer=nutzer,
    )
    nutzer.einstellung = Einstellung(
        id=200 + nutzer_id,
        nutzer_id=nutzer_id,
        newsletter_aktiv=True,
        benachrichtigungen_aktiv=True,
        sprache="de",
        nutzer=nutzer,
    )
    return NutzerDTO(nutzer)


def _nutzer_liste() -> tuple[NutzerDTO, ...]:
    return (
        _create_nutzer_dto(
            nutzer_id=1,
            version=0,
            vorname="Ada",
            nachname="Admin",
            email="admin@example.de",
            username="admin",
        ),
        _create_nutzer_dto(
            nutzer_id=20,
            version=1,
            vorname="Alice",
            nachname="Anderson",
            email="alice@example.de",
            username="alice",
        ),
        _create_nutzer_dto(
            nutzer_id=30,
            version=0,
            vorname="Bob",
            nachname="Miller",
            email="bob@example.de",
            username="bob",
        ),
        _create_nutzer_dto(
            nutzer_id=40,
            version=0,
            vorname="Charlie",
            nachname="Tester",
            email="charlie@example.de",
            username="charlie",
        ),
        _create_nutzer_dto(
            nutzer_id=60,
            version=0,
            vorname="Delete",
            nachname="Me",
            email="delete@example.de",
            username="deleteme",
        ),
    )


