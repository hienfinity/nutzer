
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
