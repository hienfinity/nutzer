"""DTO-Klasse fuer Einstellungen eines Nutzers."""

from dataclasses import dataclass

import strawberry

from nutzer.entity import Einstellung

__all__ = ["EinstellungDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class EinstellungDTO:
    """DTO-Klasse fuer Einstellungen ohne SQLAlchemy-Decorator."""

    newsletter_aktiv: bool
    benachrichtigungen_aktiv: bool
    sprache: str

    def __init__(self, einstellung: Einstellung) -> None:
        """Initialisierung von EinstellungDTO durch ein Entity-Objekt."""
        self.newsletter_aktiv = einstellung.newsletter_aktiv
        self.benachrichtigungen_aktiv = einstellung.benachrichtigungen_aktiv
        self.sprache = einstellung.sprache
