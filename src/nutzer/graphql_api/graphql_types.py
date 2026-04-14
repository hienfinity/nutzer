"""GraphQL-Typen fuer die Nutzer-Schnittstelle."""

from datetime import date

import strawberry

from nutzer.entity import Interesse, Rolle, Status

__all__ = [
    "AdresseInput",
    "CreatePayload",
    "EinstellungInput",
    "LoginResult",
    "NutzerInput",
    "Suchparameter",
]


@strawberry.input
class Suchparameter:
    """Suchparameter fuer GraphQL-Abfragen nach Nutzern."""

    nachname: str | None = None
    email: str | None = None
    username: str | None = None


@strawberry.input
class AdresseInput:
    """Adresse eines Nutzers fuer GraphQL-Mutations."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str


@strawberry.input
class EinstellungInput:
    """Einstellungen eines Nutzers fuer GraphQL-Mutations."""

    newsletter_aktiv: bool
    benachrichtigungen_aktiv: bool
    sprache: str


@strawberry.input
class NutzerInput:
    """Eingabedaten fuer das Anlegen eines neuen Nutzers."""

    vorname: str
    nachname: str
    email: str
    username: str
    telefonnummer: str | None = None
    geburtsdatum: date
    beitrittsdatum: date
    aktiv: bool
    rolle: Rolle
    status: Status
    interessen: list[Interesse]
    adresse: AdresseInput
    einstellung: EinstellungInput


@strawberry.type
class CreatePayload:
    """Rueckgabetyp fuer das erfolgreiche Anlegen eines Nutzers."""

    id: int


@strawberry.type
class LoginResult:
    """Rueckgabetyp fuer einen erfolgreichen Login."""

    token: str
    expiresIn: str  # noqa: N815  # NOSONAR
    roles: list[str]
