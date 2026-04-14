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



