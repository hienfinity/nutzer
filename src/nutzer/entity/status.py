"""Fachliches Enum fuer den Status eines Nutzers."""

from enum import StrEnum


class Status(StrEnum):
    """Moegliche Statuswerte eines Nutzers."""

    AKTIV = "AKTIV"
    """Der Nutzer ist aktiv und kann normal verwendet werden."""

    GESPERRT = "GESPERRT"
    """Der Nutzer ist gesperrt und damit eingeschraenkt."""

    INAKTIV = "INAKTIV"
    """Der Nutzer ist vorhanden, aber derzeit nicht aktiv."""
