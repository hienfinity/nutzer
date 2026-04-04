
"""Repository fuer persistente Nutzerdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from nutzer.entity import Nutzer
from nutzer.repository.pageable import Pageable
from nutzer.repository.slice import Slice

__all__ = ["NutzerRepository"]

class NutzerRepository:
    """Stellt spaeter DB-Zugriffe fuer die Entity-Klasse Nutzer bereit."""
