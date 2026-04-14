"""Tests fuer DELETE."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, delete, rest_url
from pytest import mark


@mark.rest
@mark.delete_request
def test_delete() -> None:
    # arrange
    nutzer_id: Final = 60

    # act
    response: Final = delete(
        f"{rest_url}/{nutzer_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT


@mark.rest
@mark.delete_request
def test_delete_not_found() -> None:
    # arrange
    nutzer_id: Final = 999999

    # act
    response: Final = delete(
        f"{rest_url}/{nutzer_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
