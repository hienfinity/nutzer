"""Ausschnitt gefundener Daten aus dem Repository."""

from dataclasses import dataclass
from typing import TypeVar

__all__ = ["Slice"]


T = TypeVar("T")


@dataclass(eq=False, slots=True, kw_only=True)
class Slice[T]:
    """Data class fuer einen Seitenausschnitt gefundener Daten."""

    content: tuple[T, ...]
    """Gefundene Datensaetze als Tupel."""

    total_elements: int
    """Gesamtanzahl aller passenden Datensaetze."""
