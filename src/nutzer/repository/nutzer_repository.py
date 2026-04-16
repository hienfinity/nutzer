NUTZER_ID_LOG: Final = "nutzer_id={}"  # Logging-Template für Nutzer-IDs

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
        logger.debug(NUTZER_ID_LOG, nutzer_id)

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

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Nutzer)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_email(self, email: str, session: Session) -> Nutzer | None:
        """Einen Nutzer anhand der Emailadresse suchen.

        :param email: Emailadresse
        :param session: Session für SQLAlchemy
        :return: Gefundener Nutzer, falls vorhanden, sonst None
        :rtype: Nutzer | None
        """
        logger.debug("email={}", email)

        statement: Final = (
            select(Nutzer)
            .options(
                joinedload(Nutzer.adresse),
                joinedload(Nutzer.einstellung),
            )
            .where(Nutzer.email == email)
        )
        nutzer: Final = session.scalar(statement)

        logger.debug("{}", nutzer)
        return nutzer

    def _find_by_username(self, username: str, session: Session) -> Nutzer | None:
        """Einen Nutzer anhand des Benutzernamens suchen.

        :param username: Benutzername
        :param session: Session für SQLAlchemy
        :return: Gefundener Nutzer, falls vorhanden, sonst None
        :rtype: Nutzer | None
        """
        logger.debug("username={}", username)

        statement: Final = (
            select(Nutzer)
            .options(
                joinedload(Nutzer.adresse),
                joinedload(Nutzer.einstellung),
            )
            .where(Nutzer.username == username)
        )
        nutzer: Final = session.scalar(statement)

        logger.debug("{}", nutzer)
        return nutzer

    def _find_by_nachname(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Nutzer]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size

        statement: Final = (
            (
                select(Nutzer)
                .options(
                    joinedload(Nutzer.adresse),
                    joinedload(Nutzer.einstellung),
                )
                .filter(Nutzer.nachname.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Nutzer)
                .options(
                    joinedload(Nutzer.adresse),
                    joinedload(Nutzer.einstellung),
                )
                .filter(Nutzer.nachname.ilike(f"%{teil}%"))
            )
        )

        nutzer_liste: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_nachname(teil, session)
        nutzer_slice: Final = Slice(content=tuple(nutzer_liste), total_elements=anzahl)
        logger.debug("{}", nutzer_slice)
        return nutzer_slice

    def _count_rows_nachname(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Nutzer)
            .filter(Nutzer.nachname.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_email(self, email: str, session: Session) -> bool:
        """Abfrage, ob es die Emailadresse bereits gibt.

        :param email: Emailadresse
        :param session: Session für SQLAlchemy
        :return: True, falls es die Emailadresse bereits gibt, False sonst
        :rtype: bool
        """
        logger.debug("email={}", email)

        statement: Final = select(func.count()).where(Nutzer.email == email)
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def exists_email_other_id(
        self,
        email: str,
        nutzer_id: int,
        session: Session,
    ) -> bool:
        """Abfrage, ob es die Emailadresse bei einer anderen Nutzer-ID bereits gibt.

        :param email: Emailadresse
        :param nutzer_id: eigene Nutzer-ID
        :param session: Session für SQLAlchemy
        :return: True, falls es die Emailadresse bereits gibt, False sonst
        :rtype: bool
        """
        logger.debug("email={}", email)

        statement: Final = select(Nutzer.id).where(Nutzer.email == email)
        id_db: Final = session.scalar(statement)
        logger.debug("id_db={}", id_db)
        return id_db is not None and id_db != nutzer_id

    def exists_username(self, username: str | None, session: Session) -> bool:
        """Abfrage, ob es den Benutzernamen bereits gibt.

        :param username: Benutzername
        :param session: Session für SQLAlchemy
        :return: True, falls es den Benutzernamen bereits gibt
        :rtype: bool
        """
        logger.debug("username={}", username)

        if username is None:
            return False

        statement: Final = select(Nutzer.username).filter_by(username=username)
        username_db: Final = session.scalar(statement)
        logger.debug("username_db={}", username_db)
        return username_db is not None

    def create(self, nutzer: Nutzer, session: Session) -> Nutzer:
        """Speichere einen neuen Nutzer ab.

        :param nutzer: Die Daten des neuen Nutzers ohne ID
        :param session: Session für SQLAlchemy
        :return: Der neu angelegte Nutzer mit generierter ID
        :rtype: Nutzer
        """
        logger.debug(
            "nutzer={}, nutzer.adresse={}, nutzer.einstellung={}",
            nutzer,
            nutzer.adresse,
            nutzer.einstellung,
        )

        session.add(instance=nutzer)
        session.flush(objects=[nutzer])
        logger.debug(NUTZER_ID_LOG, nutzer.id)
        return nutzer


    def update(self, nutzer: Nutzer, session: Session) -> Nutzer | None:
        """Aktualisiere einen Nutzer.

        :param nutzer: Die neuen Nutzerdaten
        :param session: Session für SQLAlchemy
        :return: Der aktualisierte Nutzer oder None, falls kein Nutzer mit der ID existiert
        :rtype: Nutzer | None
        """
        logger.debug("{}", nutzer)

        if (nutzer_db := self.find_by_id(nutzer_id=nutzer.id, session=session)) is None:
            return None

        logger.debug("{}", nutzer_db)
        return nutzer_db

    def delete_by_id(self, nutzer_id: int, session: Session) -> None:
        """Lösche die Daten zu einem Nutzer.

        :param nutzer_id: Die ID des zu löschenden Nutzers
        :param session: Session für SQLAlchemy
        """
        logger.debug(NUTZER_ID_LOG, nutzer_id)

        if (nutzer := self.find_by_id(nutzer_id=nutzer_id, session=session)) is None:
            return

        session.delete(nutzer)
        logger.debug("ok")

    def find_nachnamen(self, teil: str, session: Session) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring.

        :param teil: Teilstring zu den gesuchten Nachnamen
        :param session: Session für SQLAlchemy
        :return: Liste der gefundenen Nachnamen oder eine leere Liste
        :rtype: Sequence[str]
        """
        logger.debug("teil={}", teil)

        statement: Final = (
            select(Nutzer.nachname)
            .filter(Nutzer.nachname.ilike(f"%{teil}%"))
            .distinct()
        )
        nachnamen: Final = session.scalars(statement).all()

        logger.debug("nachnamen={}", nachnamen)
        return nachnamen
