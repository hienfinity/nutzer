"""Tests fuer Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"

@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                nutzer(nutzerId: "20") {
                    id
                    version
                    vorname
                    nachname
                    email
                    username
                    telefonnummer
                    geburtsdatum
                    beitrittsdatum
                    aktiv
                    rolle
                    status
                    interessen
                    adresse {
                        strasse
                        hausnummer
                        plz
                        ort
                    }
                    einstellung {
                        newsletterAktiv
                        benachrichtigungenAktiv
                        sprache
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    nutzer: Final = data["nutzer"]
    assert isinstance(nutzer, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                nutzer(nutzerId: "999999") {
                    nachname
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["nutzer"] is None
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_email() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                nutzerListe(suchparameter: {email: "admin@acme.com"}) {
                    id
                    version
                    vorname
                    nachname
                    email
                    username
                    telefonnummer
                    geburtsdatum
                    beitrittsdatum
                    aktiv
                    rolle
                    status
                    interessen
                    adresse {
                        strasse
                        hausnummer
                        plz
                        ort
                    }
                    einstellung {
                        newsletterAktiv
                        benachrichtigungenAktiv
                        sprache
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    nutzer_liste: Final = response_body["data"]["nutzerListe"]
    assert isinstance(nutzer_liste, list)
    assert len(nutzer_liste) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_email_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                nutzerListe(suchparameter: {email: "not.found@acme.com"}) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    nutzer_liste: Final = response_body["data"]["nutzerListe"]
    assert isinstance(nutzer_liste, list)
    assert len(nutzer_liste) == 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nachname() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                nutzerListe(suchparameter: {nachname: "Alice"}) {
                    id
                    version
                    vorname
                    nachname
                    email
                    username
                    telefonnummer
                    geburtsdatum
                    beitrittsdatum
                    aktiv
                    rolle
                    status
                    interessen
                    adresse {
                        strasse
                        hausnummer
                        plz
                        ort
                    }
                    einstellung {
                        newsletterAktiv
                        benachrichtigungenAktiv
                        sprache
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    nutzer_liste: Final = response_body["data"]["nutzerListe"]
    assert isinstance(nutzer_liste, list)
    assert len(nutzer_liste) > 0
    assert response_body.get("errors") is None
