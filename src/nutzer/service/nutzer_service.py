"""Geschaeftslogik zum Lesen von Nutzerdaten."""

from typing import Final

from loguru import logger

from nutzer.entity import Nutzer
from nutzer.repository import NutzerRepository, Session

__all__ = ["NutzerService"]


class NutzerService:
    """Service-Klasse mit Geschaeftslogik fuer Nutzer."""

    def __init__(self, repo: NutzerRepository) -> None:
        """Konstruktor mit abhaengigem NutzerRepository."""
        self.repo: NutzerRepository = repo

    def find_by_id(self, nutzer_id: int) -> Nutzer | None:
        """Einen Nutzer ueber seine ID suchen."""
        logger.debug("nutzer_id={}", nutzer_id)

        with Session() as session:
            nutzer: Final = self.repo.find_by_id(nutzer_id=nutzer_id, session=session)
            session.commit()

        logger.debug("{}", nutzer)
        return nutzer
