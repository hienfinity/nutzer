"""DTO fuer eine Seite mit paginierten Ergebnissen."""

from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from nutzer.repository.pageable import Pageable

__all__ = ["Page"]

T = TypeVar("T")


