
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
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Nutzer."""

    def find_by_id(self, nutzer_id: int | None, session: Session) -> Nutzer | None:
        """Suche mit der Nutzer-ID.

        :param nutzer_id: ID des gesuchten Nutzers
        :param session: Session für SQLAlchemy
        :return: Der gefundene Nutzer oder None
        :rtype: Nutzer | None
        """
        logger.debug("nutzer_id={}", nutzer_id)

        if nutzer_id is None:
            return None

        statement: Final = (
            select(Nutzer)
            .options(
                joinedload(Nutzer.adresse),
                joinedload(Nutzer.einstellung),
            )
            .where(Nutzer.id == nutzer_id)
        )
        nutzer: Final = session.scalar(statement)

        logger.debug("{}", nutzer)
        return nutzer

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Nutzer]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter als Dictionary
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Tupel der gefundenen Nutzer oder leeres Tupel
        :rtype: Slice[Nutzer]
        """
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)

        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        for key, value in suchparameter.items():
            if key == "email":
                nutzer = self._find_by_email(email=value, session=session)
                logger.debug(log_str, nutzer)
                return (
                    Slice(content=(nutzer,), total_elements=1)
                    if nutzer is not None
                    else Slice(content=(), total_elements=0)
                )
            if key == "nachname":
                nutzer_liste = self._find_by_nachname(
                    teil=value,
                    pageable=pageable,
                    session=session,
                )
                logger.debug(log_str, nutzer_liste)
                return nutzer_liste
            if key == "username":
                nutzer = self._find_by_username(username=value, session=session)
                logger.debug(log_str, nutzer)
                return (
                    Slice(content=(nutzer,), total_elements=1)
                    if nutzer is not None
                    else Slice(content=(), total_elements=0)
                )

        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Nutzer]:
        """Alle Nutzer mit Pagination suchen.

        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Seite mit Nutzern
        :rtype: Slice[Nutzer]
        """
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Nutzer)
                .options(
                    joinedload(Nutzer.adresse),
                    joinedload(Nutzer.einstellung),
                )
                .limit(pageable.size)
                .offset(offset)
            )
        else:
            statement: Final = select(Nutzer).options(
                joinedload(Nutzer.adresse),
                joinedload(Nutzer.einstellung),
            )

        nutzer_liste: Final = session.scalars(statement).all()
        anzahl: Final = self._count_all_rows(session)
        nutzer_slice: Final = Slice(content=tuple(nutzer_liste), total_elements=anzahl)
        logger.debug("nutzer_slice={}", nutzer_slice)
        return nutzer_slice
