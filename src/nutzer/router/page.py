"""DTO fuer eine Seite mit paginierten Ergebnissen."""

from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from nutzer.repository.pageable import Pageable

__all__ = ["Page"]

T = TypeVar("T")


@dataclass(slots=True, kw_only=True)
class Page(Generic[T]):
    """Page fuer paginierte Ergebnisse."""

    content: tuple[T, ...]
    number: int
    size: int
    total_elements: int
    total_pages: int
