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

@fixture
def nutzer_service(nutzer_repository: NutzerRepository) -> NutzerService:
    """Fixture fuer NutzerService."""
    return NutzerService(nutzer_repository)

@fixture
def keycloak_admin_mock(mocker: MockerFixture) -> KeycloakAdmin:
    """Patching von KeycloakAdmin() innerhalb von UserService."""
    keycloak_admin_cls_mock = mocker.patch(
        "nutzer.security.user_service.KeycloakAdmin"
    )
    return keycloak_admin_cls_mock.return_value
