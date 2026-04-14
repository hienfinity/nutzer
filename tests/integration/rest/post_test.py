"""Tests fuer POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, post, rest_url
from pytest import mark


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neuer_nutzer: Final = {
        "vorname": "Test",
        "nachname": "Nachnamerest",
        "email": "testrest@rest.de",
        "username": "testrest",
        "telefonnummer": "123456",
        "geburtsdatum": "2022-02-01",
        "beitrittsdatum": "2024-01-01",
        "aktiv": True,
        "rolle": "NUTZER",
        "status": "AKTIV",
        "interessen": ["TECHNIK"],
        "adresse": {
            "strasse": "Restweg",
            "hausnummer": "1",
            "plz": "99999",
            "ort": "Restort",
        },
        "einstellung": {
            "newsletter_aktiv": True,
            "benachrichtigungen_aktiv": True,
            "sprache": "de",
        },
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neuer_nutzer_invalid: Final = {
        "vorname": "",
        "nachname": "",
        "email": "falsche_email@",
        "username": "x" * 21,
        "telefonnummer": "123456",
        "geburtsdatum": "2022-02-01",
        "beitrittsdatum": "2024-01-01",
        "aktiv": True,
        "rolle": "INVALID",
        "status": "AKTIV",
        "interessen": ["TECHNIK"],
        "adresse": {
            "strasse": "",
            "hausnummer": "",
            "plz": "",
            "ort": "",
        },
        "einstellung": {
            "newsletter_aktiv": True,
            "benachrichtigungen_aktiv": True,
            "sprache": "",
        },
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_nutzer_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "vorname" in body
    assert "nachname" in body
    assert "email" in body
    assert "username" in body
    assert "strasse" in body



