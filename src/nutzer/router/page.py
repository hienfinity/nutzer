"""DTO fuer eine Seite mit paginierten Ergebnissen."""

from dataclasses import dataclass
from math import ceil

from nutzer.repository.pageable import Pageable

__all__ = ["Page"]


@dataclass(slots=True, kw_only=True)
class Page[T]:
    """Page fuer paginierte Ergebnisse."""

    content: tuple[T, ...]
    number: int
    size: int
    total_elements: int
    total_pages: int

    @staticmethod
    def create(
        content: tuple[T, ...],
        pageable: Pageable,
        total_elements: int,
    ) -> Page[T]:
        """Erzeuge eine Page auf Basis von Content, Pageable und Gesamtanzahl."""
        size = pageable.size
        total_pages = ceil(total_elements / size) if size > 0 else 1

        return Page(
            content=content,
            number=pageable.number,
            size=size,
            total_elements=total_elements,
            total_pages=total_pages,
        )
