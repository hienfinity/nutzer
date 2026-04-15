"""Tests fuer Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    nutzerInput: {
                        vorname: "Max"
                        nachname: "Graphql"
                        email: "testgraphql@graphql.de"
                        username: "testgraphql"
                        telefonnummer: "123456789"
                        geburtsdatum: "2000-01-01"
                        beitrittsdatum: "2024-01-01"
                        aktiv: true
                        rolle: NUTZER
                        status: AKTIV
                        interessen: [TECHNIK, SPORT]
                        adresse: {
                            strasse: "Teststrasse"
                            hausnummer: "10"
                            plz: "76133"
                            ort: "Karlsruhe"
                        }
                        einstellung: {
                            newsletterAktiv: true
                            benachrichtigungenAktiv: true
                            sprache: "de"
                        }
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None


@mark.graphql
@mark.mutation
def test_create_invalid() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    nutzerInput: {
                        vorname: ""
                        nachname: ""
                        email: "falsche_email@"
                        username: ""
                        telefonnummer: "123"
                        geburtsdatum: "2000-01-01"
                        beitrittsdatum: "2024-01-01"
                        aktiv: true
                        rolle: NUTZER
                        status: AKTIV
                        interessen: [TECHNIK]
                        adresse: {
                            strasse: ""
                            hausnummer: ""
                            plz: ""
                            ort: ""
                        }
                        einstellung: {
                            newsletterAktiv: true
                            benachrichtigungenAktiv: true
                            sprache: ""
                        }
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"] is None
    errors: Final = response_body["errors"]
    assert isinstance(errors, list)
    assert len(errors) == 1
