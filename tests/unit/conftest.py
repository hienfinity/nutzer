"""Fixture fuer pytest: Repository, Nutzer(Write)Service, KeycloakAdmin, UserService."""

from keycloak import KeycloakAdmin
from pytest import fixture
from pytest_mock import MockerFixture

from nutzer.repository import NutzerRepository
from nutzer.security import UserService
from nutzer.service import NutzerService, NutzerWriteService


@fixture()
def nutzer_repository() -> NutzerRepository:
    """Fixture fuer NutzerRepository."""
    return NutzerRepository()
