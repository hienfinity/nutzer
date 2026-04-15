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


@mark.unit
@mark.unit_find_by_id
def test_find_by_id(nutzer_service, session_mock) -> None:
    # Arrange
    nutzer_id = 1
    adresse_mock = Adresse(
        id=11,
        strasse="Teststrasse",
        hausnummer="10",
        plz="11111",
        ort="Mockort",
        nutzer_id=nutzer_id,
        nutzer=None,
    )
    einstellung_mock = Einstellung(
        id=21,
        newsletter_aktiv=True,
        benachrichtigungen_aktiv=True,
        sprache="de",
        nutzer_id=nutzer_id,
        nutzer=None,
    )
    nutzer_mock = Nutzer(
        id=nutzer_id,
        vorname="Max",
        nachname="Mocktest",
        email="mock@email.test",
        username="mocktest",
        telefonnummer="123456789",
        geburtsdatum=date(2000, 1, 1),
        beitrittsdatum=date(2025, 1, 31),
        aktiv=True,
        rolle=Rolle.NUTZER,
        status=Status.AKTIV,
        adresse=adresse_mock,
        einstellung=einstellung_mock,
        interessen=[Interesse.TECHNIK],
    )
    adresse_mock.nutzer = nutzer_mock
    einstellung_mock.nutzer = nutzer_mock

    nutzer_dto_mock = NutzerDTO(nutzer_mock)
    session_mock.commit.return_value = None

    # Act
    nutzer_dto = nutzer_service.find_by_id(nutzer_id=nutzer_id)

    # Assert
    assert asdict(nutzer_dto) == asdict(nutzer_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found(
    nutzer_service: NutzerService,
    session_mock,
) -> None:
    # Arrange
    nutzer_id = 999
    session_mock.commit.return_value = None

    # Repository mocken
    nutzer_service.repo.find_by_id = lambda nutzer_id, session: None

    # Act
    with raises(NotFoundError) as err:
        nutzer_service.find_by_id(nutzer_id=nutzer_id)

    # Assert
    assert err.type is NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.nutzer_id == nutzer_id
