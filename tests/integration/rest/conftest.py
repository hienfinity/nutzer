"""Fixture fuer pytest: vorbereitende Initialisierung fuer REST-Tests."""

from common_test import check_readiness, db_populate, keycloak_populate
from pytest import fixture

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    check_readiness()
    print("Appserver ist 'ready'")


@fixture(scope=session_scope, autouse=True)
def populate_per_session() -> None:
    """Fixture, um die Testdaten fuer die Session vorzubereiten."""
    db_populate()
    print("DB ist neu geladen")
    keycloak_populate()
    print("Keycloak ist neu geladen")
