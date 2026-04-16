"""Geschaeftslogik zum Lesen von Nutzerdaten."""

from collections.abc import Mapping
from typing import Final

from loguru import logger

from nutzer.repository import NutzerRepository, Pageable, Session, Slice
from nutzer.service.exceptions import NotFoundError
from nutzer.service.nutzer_dto import NutzerDTO

__all__ = ["NutzerService"]


class NutzerService:
    """Service-Klasse mit Geschaeftslogik fuer Nutzer."""

    def __init__(self, repo: NutzerRepository) -> None:
        """Konstruktor mit abhaengigem NutzerRepository."""
        self.repo: NutzerRepository = repo

    def find_by_id(self, nutzer_id: int) -> NutzerDTO:
        """Einen Nutzer ueber seine ID suchen."""
        logger.debug("nutzer_id={}", nutzer_id)

        with Session() as session:
            nutzer: Final = self.repo.find_by_id(nutzer_id=nutzer_id, session=session)
            if nutzer is None:
                logger.debug("NotFoundError fuer nutzer_id={}", nutzer_id)
                raise NotFoundError(nutzer_id=nutzer_id)
            nutzer_dto: Final = NutzerDTO(nutzer)
            session.commit()

        logger.debug("{}", nutzer_dto)
        return nutzer_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[NutzerDTO]:
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
            nutzer_dto = tuple(NutzerDTO(nutzer) for nutzer in nutzer_slice.content)
            session.commit()

        nutzer_dto_slice = Slice(
            content=nutzer_dto,
            total_elements=nutzer_slice.total_elements,
        )
        logger.debug("{}", nutzer_dto_slice)
        return nutzer_dto_slice

    def find_nachnamen(self, teil: str) -> tuple[str, ...]:
        """Nachnamen zu einem Teilstring suchen."""
        logger.debug("teil={}", teil)

        with Session() as session:
            nachnamen: Final = self.repo.find_nachnamen(teil=teil, session=session)
            if len(nachnamen) == 0:
                logger.debug("NotFoundError fuer teil={}", teil)
                raise NotFoundError()
            session.commit()

        nachnamen_tuple: Final = tuple(nachnamen)
        logger.debug("nachnamen={}", nachnamen_tuple)
        return nachnamen_tuple
