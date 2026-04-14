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


class StubReadService:
    def __init__(self, nutzer: tuple[NutzerDTO, ...]) -> None:
        self._nutzer = nutzer

    def find_by_id(self, nutzer_id: int) -> NutzerDTO:
        for eintrag in self._nutzer:
            if eintrag.id == nutzer_id:
                return eintrag
        raise NotFoundError(nutzer_id=nutzer_id)

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[NutzerDTO]:
        if not suchparameter:
            content = self._nutzer
        elif "email" in suchparameter:
            content = tuple(
                eintrag
                for eintrag in self._nutzer
                if eintrag.email == suchparameter["email"]
            )
        elif "nachname" in suchparameter:
            teil = suchparameter["nachname"].lower()
            content = tuple(
                eintrag
                for eintrag in self._nutzer
                if teil in eintrag.nachname.lower()
            )
        elif "username" in suchparameter:
            content = tuple(
                eintrag
                for eintrag in self._nutzer
                if eintrag.username == suchparameter["username"]
            )
        else:
            content = ()

        if len(content) == 0:
            raise NotFoundError()

        start = pageable.number * pageable.size
        end = None if pageable.size == 0 else start + pageable.size
        return Slice(content=content[start:end], total_elements=len(content))

    def find_nachnamen(self, teil: str) -> tuple[str, ...]:
        nachnamen = tuple(
            eintrag.nachname
            for eintrag in self._nutzer
            if teil.lower() in eintrag.nachname.lower()
        )
        if len(nachnamen) == 0:
            raise NotFoundError()
        return nachnamen


class StubWriteService:
    def __init__(self, nutzer: tuple[NutzerDTO, ...]) -> None:
        self._nutzer = nutzer

    def create(self, nutzer: Nutzer) -> NutzerDTO:
        for eintrag in self._nutzer:
            if eintrag.email == nutzer.email:
                raise EmailExistsError(nutzer.email)
            if eintrag.username == nutzer.username:
                raise UsernameExistsError(nutzer.username or "")

        nutzer.id = 1001
        nutzer.version = 0
        if nutzer.adresse is not None:
            nutzer.adresse.nutzer_id = nutzer.id
        if nutzer.einstellung is not None:
            nutzer.einstellung.nutzer_id = nutzer.id
        return NutzerDTO(nutzer)

    def update(self, nutzer: Nutzer, nutzer_id: int, version: int) -> NutzerDTO:
        nutzer_db = next((eintrag for eintrag in self._nutzer if eintrag.id == nutzer_id), None)
        if nutzer_db is None:
            raise NotFoundError(nutzer_id)
        if nutzer_db.version > version:
            raise VersionOutdatedError(version)

        for eintrag in self._nutzer:
            if eintrag.id != nutzer_id and eintrag.email == nutzer.email:
                raise EmailExistsError(nutzer.email)

        return _create_nutzer_dto(
            nutzer_id=nutzer_id,
            version=version + 1,
            vorname=nutzer.vorname,
            nachname=nutzer.nachname,
            email=nutzer.email,
            username=nutzer_db.username,
        )

    def delete_by_id(self, nutzer_id: int) -> None:
        return None


class StubTokenService:
    def token(self, username: str | None, password: str | None) -> Mapping[str, Any]:
        if (
            username is None
            or password is None
            or (username, password) not in {("admin", "p"), ("alice", "p")}
        ):
            raise LoginError(username=username)

        return {
            "access_token": f"token-{username}",
            "expires_in": 3600,
            "resource_access": {
                "python-client": {
                    "roles": ["admin"] if username == "admin" else ["nutzer"],
                }
            },
        }

    def get_roles_from_token(self, token: str | Mapping[str, Any]) -> list[Role]:
        if isinstance(token, str):
            return [Role.ADMIN] if token == "token-admin" else [Role.NUTZER]

        roles = token["resource_access"]["python-client"]["roles"]
        return [Role[rolle.upper()] for rolle in roles]

    def get_user_from_request(self, _request: Any) -> User:
        return User(
            username="admin",
            email="admin@example.de",
            nachname="Admin",
            vorname="Ada",
            roles=[Role.ADMIN],
        )


def _to_path(url: str) -> str:
    return url.removeprefix(base_url)


def _request(method: str, url: str, **kwargs: Any) -> Any:
    kwargs.pop("verify", None)
    kwargs.pop("timeout", None)

    nutzer = _nutzer_liste()
    app.dependency_overrides[get_service] = lambda: StubReadService(nutzer)
    app.dependency_overrides[get_write_service] = lambda: StubWriteService(nutzer)
    app.dependency_overrides[get_token_service] = lambda: StubTokenService()

    try:
        with TestClient(app) as client:
            return client.request(method=method, url=_to_path(url), **kwargs)
    finally:
        app.dependency_overrides.clear()


def check_readiness() -> None:
    response: Final = get(health_url, verify=ctx)
    if response.status_code != 200:
        raise RuntimeError(f"health mit Statuscode {response.status_code}")


def login(
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    login_data: Final = {"username": username, "password": password}
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != 200:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")
    response_body: Final = response.json()
    token: Final = response_body.get("token")
    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login() mit ungueltigem Token: type={type(token)}")
    return token


def db_populate() -> None:
    return None


def keycloak_populate() -> None:
    return None


def get(url: str, **kwargs: Any) -> Any:
    return _request("GET", url, **kwargs)


def post(url: str, **kwargs: Any) -> Any:
    return _request("POST", url, **kwargs)


def put(url: str, **kwargs: Any) -> Any:
    return _request("PUT", url, **kwargs)


def delete(url: str, **kwargs: Any) -> Any:
    return _request("DELETE", url, **kwargs)
