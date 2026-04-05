"""DTO-Klasse fuer die Adresse eines Nutzers."""

from dataclasses import dataclass

import strawberry

from nutzer.entity import Adresse

__all__ = ["AdresseDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AdresseDTO:
    """DTO-Klasse fuer die Adresse ohne SQLAlchemy-Decorator."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str

    def __init__(self, adresse: Adresse) -> None:
        """Initialisierung von AdresseDTO durch ein Entity-Objekt."""
        self.strasse = adresse.strasse
        self.hausnummer = adresse.hausnummer
        self.plz = adresse.plz
        self.ort = adresse.ort
