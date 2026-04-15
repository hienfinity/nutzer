"""Unit-Tests fuer find_by_id() von NutzerService."""

from dataclasses import asdict
from datetime import date
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from nutzer.entity import Adresse, Einstellung, Interesse, Nutzer, Rolle, Status
from nutzer.service import NotFoundError, NutzerDTO, NutzerService

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: "MockerFixture"):
    session = mocker.Mock()
    # Patching von "with Session() as session:" in nutzer_service.py
    mocker.patch(
        "nutzer.service.nutzer_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session