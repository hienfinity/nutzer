"""Tests fuer GET mit Pfadparameter fuer die ID."""

from http import HTTPStatus
from typing import Final

from common_test import auth_headers, ctx, get, rest_url
from pytest import mark


@mark.rest
@mark.get_request
def test_get_by_id() -> None:
    # arrange
    nutzer_id: Final = 20
    headers: Final = auth_headers()

    # act
    response: Final = get(f"{rest_url}/{nutzer_id}", headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == nutzer_id


@mark.rest
@mark.get_request
def test_get_by_id_not_found() -> None:
    # arrange
    nutzer_id: Final = 999999
    headers: Final = auth_headers()

    # act
    response: Final = get(f"{rest_url}/{nutzer_id}", headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_etag() -> None:
    # arrange
    nutzer_id: Final = 20
    headers = auth_headers()
    headers["If-None-Match"] = '"1"'

    # act
    response: Final = get(
        f"{rest_url}/{nutzer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
def test_get_by_id_etag_invalid() -> None:
    # arrange
    nutzer_id: Final = 20
    headers = auth_headers()
    headers["If-None-Match"] = "xxx"

    # act
    response: Final = get(
        f"{rest_url}/{nutzer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == nutzer_id
