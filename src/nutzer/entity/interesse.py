"""Fachliches Enum fuer Interessen eines Nutzers."""

from enum import StrEnum


class Interesse(StrEnum):
    """Moegliche Interessen eines Nutzers."""

    TECHNIK = "TECHNIK"
    """Interesse an technischen Themen."""

    SPORT = "SPORT"
    """Interesse an Sport."""

    MUSIK = "MUSIK"
    """Interesse an Musik."""

    REISEN = "REISEN"
    """Interesse an Reisen."""
