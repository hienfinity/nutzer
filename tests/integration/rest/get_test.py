"""Tests fuer GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, get, rest_url
from pytest import mark


@mark.rest
@mark.get_request
def test_get_by_email() -> None:
    # arrange
    params = {"email": "alice@example.de"}

    # act
    response: Final = get(rest_url, params=params, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 1
    nutzer = content[0]
    assert nutzer is not None
    assert nutzer.get("email") == "alice@example.de"
    assert nutzer.get("id") == 20


@mark.rest
@mark.get_request
def test_get_by_email_not_found() -> None:
    # arrange
    params = {"email": "nicht@vorhanden.de"}

    # act
    response: Final = get(rest_url, params=params, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_nachname() -> None:
    # arrange
    params = {"nachname": "son"}

    # act
    response: Final = get(rest_url, params=params, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    for nutzer in content:
        nachname = nutzer.get("nachname")
        assert nachname is not None and isinstance(nachname, str)
        assert "son" in nachname.lower()
        assert nutzer.get("id") is not None


@mark.rest
@mark.get_request
def test_get_by_nachname_not_found() -> None:
    # arrange
    params = {"nachname": "Nichtvorhanden"}

    # act
    response: Final = get(rest_url, params=params, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND



