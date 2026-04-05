"""Geschaeftslogik zum Lesen von Nutzerdaten."""

from collections.abc import Mapping
from typing import Final

from loguru import logger

from nutzer.entity import Nutzer
from nutzer.repository import NutzerRepository, Pageable, Session, Slice
from nutzer.service.exceptions import NotFoundError

__all__ = ["NutzerService"]


class NutzerService:
    """Service-Klasse mit Geschaeftslogik fuer Nutzer."""

    def __init__(self, repo: NutzerRepository) -> None:
        """Konstruktor mit abhaengigem NutzerRepository."""
        self.repo: NutzerRepository = repo

    def find_by_id(self, nutzer_id: int) -> Nutzer:
        """Einen Nutzer ueber seine ID suchen."""
        logger.debug("nutzer_id={}", nutzer_id)

        with Session() as session:
            nutzer: Final = self.repo.find_by_id(nutzer_id=nutzer_id, session=session)
            if nutzer is None:
                logger.debug("NotFoundError fuer nutzer_id={}", nutzer_id)
                raise NotFoundError(nutzer_id=nutzer_id)
            session.commit()

        logger.debug("{}", nutzer)
        return nutzer

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[Nutzer]:
        """Nutzer mit Suchparametern suchen."""
        logger.debug("{}", suchparameter)

        with Session() as session:
            nutzer_slice: Final = self.repo.find(
                suchparameter=suchparameter,
                pageable=pageable,
                session=session,
            )
            if len(nutzer_slice.content) == 0:
                raise NotFoundError()
            session.commit()

        logger.debug("{}", nutzer_slice)
        return nutzer_slice
