"""DTO-Klasse fuer Nutzerdaten ohne SQLAlchemy-Decorator."""

from dataclasses import dataclass
from datetime import date, datetime

import strawberry

from nutzer.entity import Interesse, Nutzer, Rolle, Status
from nutzer.service.adresse_dto import AdresseDTO
from nutzer.service.einstellung_dto import EinstellungDTO

__all__ = ["NutzerDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class NutzerDTO:
    """DTO-Klasse fuer gelesene oder gespeicherte Nutzerdaten."""

    id: int
    version: int
    vorname: str
    nachname: str
    email: str
    username: str
    telefonnummer: str | None
    geburtsdatum: date
    beitrittsdatum: date
    aktiv: bool
    rolle: Rolle
    status: Status
    interessen: list[Interesse]
    adresse: AdresseDTO
    einstellung: EinstellungDTO
    erzeugt: datetime | None
    aktualisiert: datetime | None

    def __init__(self, nutzer: Nutzer) -> None:
        """Initialisierung von NutzerDTO durch ein Entity-Objekt."""
        nutzer_id = nutzer.id
        self.id = nutzer_id if nutzer_id is not None else -1
        self.version = nutzer.version
        self.vorname = nutzer.vorname
        self.nachname = nutzer.nachname
        self.email = nutzer.email
        self.username = nutzer.username
        self.telefonnummer = nutzer.telefonnummer
        self.geburtsdatum = nutzer.geburtsdatum
        self.beitrittsdatum = nutzer.beitrittsdatum
        self.aktiv = nutzer.aktiv
        self.rolle = nutzer.rolle
        self.status = nutzer.status
        self.interessen = list(nutzer.interessen)
        self.adresse = AdresseDTO(nutzer.adresse)
        self.einstellung = EinstellungDTO(nutzer.einstellung)
        self.erzeugt = nutzer.erzeugt
        self.aktualisiert = nutzer.aktualisiert
