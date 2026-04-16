"""Parameter fuer Pagination im Repository."""

from dataclasses import dataclass
from typing import Final

__all__ = ["MAX_PAGE_SIZE", "Pageable"]


DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_NUMBER = 0


@dataclass(eq=False, slots=True, kw_only=True)
class Pageable:
    """Data class fuer Seitennummer und Seitengroesse."""

    size: int
    """Anzahl Datensaetze pro Seite."""

    number: int
    """Seitennummer."""

    @staticmethod
    def create(number: str | None = None, size: str | None = None) -> Pageable:
        """Ein Pageable-Objekt aus String-Eingaben erzeugen."""
        number_int: Final = (
            DEFAULT_PAGE_NUMBER
            if number is None or not number.isdigit()
            else int(number)
        )
        size_int: Final = (
            DEFAULT_PAGE_SIZE
            if size is None
            or not size.isdigit()
            or int(size) > MAX_PAGE_SIZE
            or int(size) < 0
            else int(size)
        )
        return Pageable(size=size_int, number=number_int)
