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



