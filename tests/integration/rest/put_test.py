"""Tests fuer PUT."""

from http import HTTPStatus
from typing import Final

from common_test import auth_headers, ctx, put, rest_url
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
    headers = auth_headers()
    headers["If-Match"] = if_match

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


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    nutzer_id: Final = 40
    geaenderter_nutzer_invalid: Final = {
        "vorname": "",
        "nachname": "",
        "email": "falsche_email_put@",
        "telefonnummer": "654321",
        "geburtsdatum": "2022-02-04",
        "beitrittsdatum": "2024-02-04",
        "aktiv": False,
        "rolle": "UNGUELTIG",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = '"0"'

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "vorname" in response.text
    assert "nachname" in response.text
    assert "email" in response.text
    assert "rolle" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    nutzer_id: Final = 999999
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-03",
        "beitrittsdatum": "2024-01-03",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = '"0"'

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_email_exists() -> None:
    # arrange
    nutzer_id: Final = 40
    email_exists: Final = "alice@example.de"
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": email_exists,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-09",
        "beitrittsdatum": "2024-01-09",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = '"0"'

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "Email already exists" in response.text


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    nutzer_id: Final = 40
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-03",
        "beitrittsdatum": "2024-01-03",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=auth_headers(),
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    nutzer_id: Final = 40
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-03",
        "beitrittsdatum": "2024-01-03",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = '"-1"'

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    nutzer_id: Final = 40
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-03",
        "beitrittsdatum": "2024-01-03",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = '"xy"'

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    nutzer_id: Final = 40
    geaenderter_nutzer: Final = {
        "vorname": "Alicia",
        "nachname": "Testerput",
        "email": EMAIL_UPDATE,
        "telefonnummer": "654321",
        "geburtsdatum": "2022-01-03",
        "beitrittsdatum": "2024-01-03",
        "aktiv": False,
        "rolle": "NUTZER",
        "status": "AKTIV",
    }
    headers = auth_headers()
    headers["If-Match"] = "0"

    # act
    response: Final = put(
        f"{rest_url}/{nutzer_id}",
        json=geaenderter_nutzer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
