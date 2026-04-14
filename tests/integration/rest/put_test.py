"""Tests fuer PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, put, rest_url
from pytest import mark

EMAIL_UPDATE: Final = "alice@example.de.put"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    nutzer_id: Final = 40
    if_match: Final = '"0"'
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-09",
        "beitrittsdatum": "2024-01-09",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = {"If-Match": if_match}

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text



