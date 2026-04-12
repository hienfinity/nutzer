"""Geschaeftslogik zum Schreiben von Nutzerdaten."""

from typing import Final

from loguru import logger

from nutzer.entity import Nutzer
from nutzer.repository import NutzerRepository, Session
from nutzer.security.user_service import UserService
from nutzer.service.exceptions import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from nutzer.service.nutzer_dto import NutzerDTO

__all__ = ["NutzerWriteService"]
class NutzerWriteService:
    """Service-Klasse mit Geschaeftslogik fuer Nutzer."""

    def __init__(self, repo: NutzerRepository, user_service: UserService) -> None:
        """Konstruktor mit abhaengigem NutzerRepository."""
        self.repo: NutzerRepository = repo
        self.user_service: UserService = user_service

    def create(self, nutzer: Nutzer) -> NutzerDTO:
        """Einen neuen Nutzer anlegen.

        :param nutzer: Der neue Nutzer ohne ID
        :return: Der neu angelegte Nutzer mit generierter ID
        :rtype: NutzerDTO
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug(
            "nutzer={}, adresse={}, einstellung={}",
            nutzer,
            nutzer.adresse,
            nutzer.einstellung,
        )

        with Session() as session:
            email: Final = nutzer.email
            if self.repo.exists_email(email=email, session=session):
                raise EmailExistsError(email=email)

            username: Final = nutzer.username
            if self.repo.exists_username(username=username, session=session):
                raise UsernameExistsError(username)

            nutzer_db: Final = self.repo.create(nutzer=nutzer, session=session)
            nutzer_dto: Final = NutzerDTO(nutzer_db)
            session.commit()

        logger.debug("nutzer_dto={}", nutzer_dto)
        return nutzer_dto

    def update(self, nutzer: Nutzer, nutzer_id: int, version: int) -> NutzerDTO:
        """Daten eines Nutzers aendern.

        :param nutzer: Die neuen Daten
        :param nutzer_id: ID des zu aktualisierenden Nutzers
        :param version: Version fuer optimistische Synchronisation
        :return: Der aktualisierte Nutzer
        :rtype: NutzerDTO
        :raises NotFoundError: Falls der zu aktualisierende Nutzer nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug("nutzer_id={}, version={}, {}", nutzer_id, version, nutzer)

        with Session() as session:
            if (
                nutzer_db := self.repo.find_by_id(
                    nutzer_id=nutzer_id,
                    session=session,
                )
            ) is None:
                raise NotFoundError(nutzer_id)

            if nutzer_db.version > version:
                raise VersionOutdatedError(version)

            email: Final = nutzer.email
            if email != nutzer_db.email and self.repo.exists_email_other_id(
                nutzer_id=nutzer_id,
                email=email,
                session=session,
            ):
                raise EmailExistsError(email)

            username: Final = nutzer.username
            if username != nutzer_db.username and self.repo.exists_username(
                username=username,
                session=session,
            ):
                raise UsernameExistsError(username)

            nutzer_db.set(nutzer)
            if (
                nutzer_updated := self.repo.update(
                    nutzer=nutzer_db,
                    session=session,
                )
            ) is None:
                raise NotFoundError(nutzer_id)

            nutzer_dto: Final = NutzerDTO(nutzer_updated)
            logger.debug("{}", nutzer_dto)

            session.commit()
            nutzer_dto.version += 1
            return nutzer_dto

    def delete_by_id(self, nutzer_id: int) -> None:
        """Einen Nutzer anhand seiner ID loeschen.

        :param nutzer_id: ID des zu loeschenden Nutzers
        """
        logger.debug("nutzer_id={}", nutzer_id)

        with Session() as session:
            self.repo.delete_by_id(nutzer_id=nutzer_id, session=session)
            session.commit()
