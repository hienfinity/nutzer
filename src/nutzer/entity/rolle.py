"""Fachliches Enum fuer Rollen in der Domaene Nutzer."""

from enum import StrEnum


class Rolle(StrEnum):
    """Moegliche Rollen eines Nutzers."""

    ADMIN = "ADMIN"
    """Rolle fuer administrative Nutzer."""

    NUTZER = "NUTZER"
    """Standardrolle fuer normale Nutzer."""
