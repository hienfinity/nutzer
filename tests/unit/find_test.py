"""Unit-Tests fuer ``find()`` von ``NutzerService``."""

from datetime import date

from pytest import fixture, mark
from pytest_mock import MockerFixture

from nutzer.entity import Adresse, Einstellung, Interesse, Nutzer, Rolle, Status
from nutzer.repository import Pageable, Slice


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "nutzer.service.nutzer_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_find
def test_find_by_nachname(nutzer_service, session_mock) -> None:
    # arrange
    nachname = "Mocktest"
    nutzer_id = 1
    adresse_mock = Adresse(
        id=1,
        strasse="Mockstrasse",
        hausnummer="1a",
        plz="11111",
        ort="Mockort",
        nutzer_id=nutzer_id,
        nutzer=None,
    )
    einstellung_mock = Einstellung(
        id=1,
        newsletter_aktiv=True,
        benachrichtigungen_aktiv=True,
        sprache="de",
        nutzer_id=nutzer_id,
        nutzer=None,
    )
    nutzer_mock = Nutzer(
        id=nutzer_id,
        version=0,
        vorname="Mock",
        nachname=nachname,
        email="mock@email.test",
        username="mocktest",
        telefonnummer="123456",
        geburtsdatum=date(2025, 1, 31),
        beitrittsdatum=date(2026, 1, 31),
        aktiv=True,
        rolle=Rolle.NUTZER,
        status=Status.AKTIV,
        interessen=[Interesse.TECHNIK],
        adresse=adresse_mock,
        einstellung=einstellung_mock,
        erzeugt=None,
        aktualisiert=None,
    )
    adresse_mock.nutzer = nutzer_mock
    einstellung_mock.nutzer = nutzer_mock
    suchparameter = {"nachname": nachname}
    pageable = Pageable(size=5, number=0)
    session_mock.commit.return_value = None
    session_mock.find.return_value = None
    nutzer_slice = Slice(content=(nutzer_mock,), total_elements=1)

    nutzer_service.repo.find = session_mock.find
    session_mock.find.return_value = nutzer_slice

    # act
    nutzer_dto_slice = nutzer_service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    # assert
    assert len(nutzer_dto_slice.content) == 1
    assert nutzer_dto_slice.content[0].nachname == nachname
